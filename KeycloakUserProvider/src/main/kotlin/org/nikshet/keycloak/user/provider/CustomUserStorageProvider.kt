package org.nikshet.keycloak.user.provider

import kotlinx.coroutines.runBlocking
import org.keycloak.component.ComponentModel
import org.keycloak.credential.CredentialInput
import org.keycloak.credential.CredentialInputUpdater
import org.keycloak.credential.CredentialInputValidator
import org.keycloak.models.*
import org.keycloak.models.cache.CachedUserModel
import org.keycloak.models.cache.OnUserCache
import org.keycloak.models.credential.PasswordCredentialModel
import org.keycloak.storage.StorageId
import org.keycloak.storage.UserStorageProvider
import org.keycloak.storage.user.UserLookupProvider
import org.keycloak.storage.user.UserQueryProvider
import org.keycloak.storage.user.UserRegistrationProvider
import java.util.stream.Stream


class CustomUserStorageProvider(
    private val session: KeycloakSession,
    private val model: ComponentModel
) : UserStorageProvider, UserLookupProvider, UserRegistrationProvider, CredentialInputValidator,
    UserQueryProvider, CredentialInputUpdater, OnUserCache {

    private val service = ExternalUserService("http://nginx/base_api/v1/user-provider")

    override fun preRemove(realm: RealmModel?) {
    }

    override fun preRemove(realm: RealmModel?, group: GroupModel?) {
    }

    override fun preRemove(realm: RealmModel?, role: RoleModel?) {
    }


    override fun getUserByUsername(realm: RealmModel, username: String): UserModel? {
        val userData = runBlocking {
            service.getUserByUsername(username)
        } ?: return null

        val user = ExternalUser(
            "f:${model.id}:${userData.id}",
            userData.username,
            userData.email,
            userData.full_name,
            userData.created_at
        )

        return CustomUserAdapter(session, realm, model, user, service)
    }

    override fun getUserById(realm: RealmModel, id: String): UserModel? {
        val externalId = StorageId.externalId(id)
        val userData = runBlocking { service.getUserById(externalId) } ?: return null
        val user = ExternalUser(
            id,
            userData.username,
            userData.email,
            userData.full_name,
            userData.created_at
        )
        return CustomUserAdapter(session, realm, model, user, service)
    }

    override fun getUserByEmail(realm: RealmModel, email: String): UserModel? = null

    override fun addUser(realm: RealmModel, username: String): UserModel {
        val externalUser = ExternalUserCreation(username, "", "", "")
        val userInfo = runBlocking {
            service.createUser(
                externalUser
            )
        }

        val user = ExternalUser(
            "f:${model.id}:${userInfo.id}",
            userInfo.username,
            userInfo.email,
            userInfo.full_name,
            userInfo.created_at
        )

        return CustomUserAdapter(session, realm, model, user, service)
    }

    override fun removeUser(realm: RealmModel?, user: UserModel?): Boolean {
        if (user == null) {
            return false
        }

        val externalId = StorageId.externalId(user.id)

        runBlocking {
            service.deleteUser(externalId)
        }
        return true
    }

    override fun supportsCredentialType(credentialType: String?) =
        credentialType == PasswordCredentialModel.TYPE

    override fun updateCredential(p0: RealmModel?, p1: UserModel?, p2: CredentialInput?): Boolean {
        return false
    }

    override fun disableCredentialType(p0: RealmModel?, p1: UserModel?, p2: String?) {
        TODO("Not yet implemented")
    }

    override fun getDisableableCredentialTypesStream(p0: RealmModel?, p1: UserModel?): Stream<String> {
        return Stream.empty()
    }

    override fun isConfiguredFor(realm: RealmModel, user: UserModel, credentialType: String?) =
        credentialType == PasswordCredentialModel.TYPE

    override fun isValid(realm: RealmModel, user: UserModel, input: CredentialInput): Boolean {
        return input.type == PasswordCredentialModel.TYPE && runBlocking {
            service.validateCredentials(StorageId.externalId(user.id), input.challengeResponse)
        }
    }

    override fun close() {}

    override fun onCache(p0: RealmModel?, p1: CachedUserModel?, p2: UserModel?) {
    }

    override fun searchForUserStream(
        realm: RealmModel?,
        params: MutableMap<String, String>?,
        firstResult: Int?,
        maxResult: Int?
    ): Stream<UserModel> {
        if (realm == null) {
            return Stream.empty()
        }

        val users = runBlocking { service.getUsers() }

        return (users.stream().map { user ->
            ExternalUser(
                "f:${model.id}:${user.id}",
                user.username,
                user.email,
                user.full_name,
                user.created_at
            )
        }).map { user -> CustomUserAdapter(session, realm, model, user, service) }
    }

    override fun getGroupMembersStream(p0: RealmModel?, p1: GroupModel?, p2: Int?, p3: Int?): Stream<UserModel> {
        return Stream.empty()
    }

    override fun searchForUserByUserAttributeStream(realm: RealmModel?, p1: String?, p2: String?): Stream<UserModel> {
        return Stream.empty()
    }

    override fun getUsersCount(realm: RealmModel?): Int {
        val users = runBlocking { service.getUsers() }
        return users.size
    }


    fun getId(): String {
        return model.id
    }
}

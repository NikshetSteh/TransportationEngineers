package org.nikshet.keycloak.user.provider


import kotlinx.coroutines.runBlocking
import org.keycloak.component.ComponentModel
import org.keycloak.models.KeycloakSession
import org.keycloak.models.RealmModel
import org.keycloak.storage.StorageId
import org.keycloak.storage.adapter.AbstractUserAdapterFederatedStorage
import java.util.stream.Stream

class CustomUserAdapter(
    session: KeycloakSession,
    realm: RealmModel,
    model: ComponentModel,
    private var user: ExternalUser,
    private val service: ExternalUserService,
) : AbstractUserAdapterFederatedStorage(session, realm, model) {
    init {
        storageId = StorageId(model.id, user.id)
    }

    override fun getId() = user.id

    override fun getUsername(): String {
        return user.username
    }

    override fun setUsername(username: String?) {
        setSingleAttribute("username", username)
    }

    override fun getEmail(): String {
        return user.email
    }

    override fun setEmail(email: String?) {
        if (email != null) {
            user = user.copy(email = email)
            runBlocking {
                service.updateUser(user, StorageId.externalId(id))
            }
        }
    }

    override fun getFirstAttribute(name: String?): String? {
        return getAttributes()[name]?.get(0)
    }

    override fun setSingleAttribute(name: String?, value: String?) {
        if (name == "fullName" && value != null) {
            user = user.copy(full_name = value)
            runBlocking {
                service.updateUser(user, StorageId.externalId(id))
            }
        }
    }

    override fun removeAttribute(name: String?) {
        if (name == "fullName") {
            user = user.copy(full_name = "")
            runBlocking {
                service.updateUser(user, StorageId.externalId(id))
            }
        }
    }

    override fun getAttributes(): MutableMap<String, List<String>> {
        val attrs = mutableMapOf<String, List<String>>()
        attrs["ENABLED"] = listOf("true")
        attrs["EMAIL_VERIFIED"] = listOf("true")
        attrs["username"] = listOf(user.username)
        attrs["fullName"] = listOf(user.full_name)
        attrs["email"] = listOf(user.email)
        attrs["created_at"] = listOf(user.created_at)
        return attrs
    }

    override fun setAttribute(name: String?, values: List<String>?) {
        runBlocking {
            if (name == "fullName" && !values.isNullOrEmpty()) {
                user = user.copy(full_name = values[0])
            }
            if (name == "email" && !values.isNullOrEmpty()) {
                user = user.copy(email = values[0])
            }
            service.updateUser(user, StorageId.externalId(id))
        }
    }

    override fun getAttributeStream(name: String): Stream<String> {
        val result = getAttributes()[name]
        return if ((result == null)) Stream.empty() else result.stream()
    }
}

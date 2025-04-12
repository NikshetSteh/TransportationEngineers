package org.nikshet.keycloak.user.provider

import org.keycloak.component.ComponentModel
import org.keycloak.models.KeycloakSession
import org.keycloak.storage.UserStorageProviderFactory

class CustomUserStorageProviderFactory : UserStorageProviderFactory<CustomUserStorageProvider> {
    override fun getId(): String = "custom-user-provider"

    override fun create(session: KeycloakSession, model: ComponentModel): CustomUserStorageProvider {
        return CustomUserStorageProvider(session, model)
    }
}

package org.nikshet.keycloak.user.provider

import kotlinx.serialization.Serializable

@Serializable
data class ExternalUserCreation(
    val username: String,
    val email: String,
    val full_name: String,
    val password: String
)

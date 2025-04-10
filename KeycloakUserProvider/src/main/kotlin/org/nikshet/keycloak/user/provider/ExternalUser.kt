package org.nikshet.keycloak.user.provider

import kotlinx.serialization.Serializable

@Serializable
data class ExternalUser(
    val id: String,
    val username: String,
    val email: String,
    val full_name: String,
    val created_at: String
)

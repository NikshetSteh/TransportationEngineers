package org.nikshet.keycloak.user.provider

import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json

class ExternalUserService(
    private val baseUrl: String,
) {
    private val client = HttpClient {
        install(ContentNegotiation) {
            json(Json {
                prettyPrint = true
                isLenient = true
            })
        }
    }


    suspend fun getUserByUsername(username: String): ExternalUser? {
        return try {
            val response = client.get("$baseUrl/users/username/$username")
            if (response.status == HttpStatusCode.NotFound) {
                return null
            }
            return response.body()
        } catch (e: Exception) {
            println("Something went wrong: $e")
            null
        }
    }

    suspend fun getUserById(id: String): ExternalUser? {
        return try {
            client.get("$baseUrl/users/id/$id").body()
        } catch (e: Exception) {
            null
        }
    }

    suspend fun validateCredentials(userId: String, password: String): Boolean {
        val response: HttpResponse = client.get("$baseUrl/users/validate") {
            contentType(ContentType.Application.Json)
            setBody(mapOf("user_id" to userId, "password" to password))
        }
        return response.body<Map<String, Boolean>>()["valid"] == true
    }

    suspend fun createUser(user: ExternalUserCreation): ExternalUser {
        return client.post("$baseUrl/users") {
            contentType(ContentType.Application.Json)
            setBody(user)
        }.body()
    }

    suspend fun updateUser(user: ExternalUser, userId: String): ExternalUser {
        return client.patch("$baseUrl/users/${userId}") {
            contentType(ContentType.Application.Json)
            setBody(user)
        }.body()
    }

    suspend fun deleteUser(userId: String) {
        val response = client.delete("$baseUrl/users/$userId")
        if (!response.status.isSuccess()) {
            throw Exception("Failed to delete user: $userId")
        }
    }

    suspend fun getUsers(): List<ExternalUser> {
        return client.get("$baseUrl/users/all").body()
    }
}

plugins {
    kotlin("jvm") version "2.1.0"
    kotlin("plugin.serialization") version "1.9.0"
    id("com.github.johnrengelman.shadow") version "8.1.1"
}

group = "org.nikshet.keycloak.user.provider"
version = "1.0"

repositories {
    mavenCentral()
}

val ktorVersion = "3.1.2"
val keycloakVersion = "26.1.4"

dependencies {
    implementation("io.ktor:ktor-client-core:$ktorVersion")
    implementation("io.ktor:ktor-client-cio:$ktorVersion")
    implementation("io.ktor:ktor-client-content-negotiation:$ktorVersion")
    implementation("io.ktor:ktor-serialization-kotlinx-json:$ktorVersion")

    implementation(enforcedPlatform("org.keycloak:keycloak-parent:$keycloakVersion"))
    compileOnly("org.keycloak:keycloak-model-jpa")
}

kotlin {
    jvmToolchain(19)
}

tasks.named<com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar>("shadowJar") {
    archiveBaseName.set("custom-user-provider")
    archiveVersion.set("1.0")
    archiveClassifier.set("") // No "-all" suffix

    // Optional: Add manifest attributes
    manifest {
        attributes(
            "Implementation-Title" to project.name,
            "Implementation-Version" to project.version
        )
    }
}

// Optionally, make shadowJar the default jar task
tasks {
    build {
        dependsOn(shadowJar)
    }
}



//plugins {
//    kotlin("jvm") version "2.1.0"
//    id("com.github.johnrengelman.shadow") version "8.1.1"
//}
//
//group = "org.nikshet.keycloak.user.provider"
//version = "1.0-SNAPSHOT"
//
//repositories {
//    mavenCentral()
//}
//
//val ktorVersion = "3.1.2"
//val keycloakVersion = "26.1.4"
//
//dependencies {
//    implementation("io.ktor:ktor-client-core:$ktorVersion")
//    implementation("io.ktor:ktor-client-cio:$ktorVersion")
//    implementation("io.ktor:ktor-client-content-negotiation:$ktorVersion")
//    implementation("io.ktor:ktor-serialization-kotlinx-json:$ktorVersion")
//
//    // Import BOM (Bill of Materials) for Keycloak
//    implementation(enforcedPlatform("org.keycloak:keycloak-parent:$keycloakVersion"))
//
//    // Add keycloak-model-jpa with 'provided' scope equivalent
//    compileOnly("org.keycloak:keycloak-model-jpa")
//}
//
//kotlin {
//    jvmToolchain(19)
//}
//
//
//
////    // Keycloak SPI
////    compileOnly("org.keycloak:keycloak-server-spi:$keycloakVersion")
////    compileOnly("org.keycloak:keycloak-server-spi-private:$keycloakVersion")
////    compileOnly("org.keycloak:keycloak-model-legacy:$keycloakVersion")
////
////    // Needed for Quarkus at runtime
////    runtimeOnly("org.keycloak:keycloak-server-spi:$keycloakVersion")
////    runtimeOnly("org.keycloak:keycloak-model-legacy:$keycloakVersion")
//
////dependencies {
////    testImplementation("org.jetbrains.kotlin:kotlin-test")
////
////    val ktorVersion = "3.1.2"
////    implementation("io.ktor:ktor-client-core:$ktorVersion")
////    implementation("io.ktor:ktor-client-cio:$ktorVersion") // CIO engine
////    implementation("io.ktor:ktor-client-content-negotiation:$ktorVersion")
////    implementation("io.ktor:ktor-serialization-kotlinx-json:$ktorVersion")
////
////    val keycloakVersion = "22.0.0"
////    implementation("org.keycloak:keycloak-model-legacy:$keycloakVersion")
////
//////        <dependency>
//////      <groupId>org.apache.httpcomponents</groupId>
//////      <artifactId>httpclient</artifactId>
//////      <version></version>
//////    </dependency>
//////    implementation("org.apache.httpcomponents:httpclient:4.5.14")
////
////    // <dependency>
////    //    <groupId>org.keycloak</groupId>
////    //    <artifactId>keycloak-model-legacy</artifactId>
////    //    <version>22.0.0</version>
////    //</dependency>
////}
//
////tasks.register<Jar>("providerJar") {
////    archiveClassifier.set("keycloak-user-storage")
////    from(sourceSets.main.get().output)
////    dependsOn(configurations.runtimeClasspath)
////
////    manifest {
////        attributes(
////            "Implementation-Title" to project.name,
////            "Implementation-Version" to project.version
////        )
////    }
////}
////
////tasks.register<Jar>("providerJar") {
////    archiveClassifier.set("keycloak-user-storage")
////    from(sourceSets.main.get().output)
////
////    // Include all runtime dependencies as unpacked JAR contents
////    dependsOn(configurations.runtimeClasspath)
////    from({
////        configurations.runtimeClasspath.get()
////            .filter { it.name.endsWith("jar") }
////            .map { zipTree(it) }
////    })
////
////    manifest {
////        attributes(
////            "Implementation-Title" to project.name,
////            "Implementation-Version" to project.version,
////            "Main-Class" to "your.main.Class" // optional if you want to make it executable
////        )
////    }
////}
//
////tasks.named<com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar>("shadowJar") {
////    archiveClassifier.set("keycloak-user-storage")
////    from(sourceSets.main.get().output)
//////    dependsOn(configurations.runtimeClasspath)
////
////    manifest {
////        attributes(
////            "Implementation-Title" to project.name,
////            "Implementation-Version" to project.version
////        )
////    }
//
////    shadowJar {
////        archiveBaseName.set("user-provider")  // Name of the JAR file
////        archiveVersion.set("1.0")  // Version of the JAR file
////        archiveClassifier.set("")  // Optional: You can leave this empty to avoid extra suffix
////    }
////}
//
////tasks.named<com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar>("shadowJar") {
////    archiveClassifier.set("keycloak-user-storage") // creates `*-keycloak-user-storage.jar`
////    mergeServiceFiles() // for SPI support
////    manifest {
////        attributes(
////            "Implementation-Title" to project.name,
////            "Implementation-Version" to project.version
////        )
////    }
////}
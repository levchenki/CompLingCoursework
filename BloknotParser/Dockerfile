FROM maven:3.8.1-openjdk-17-slim as MAVEN_BUILD

COPY ./ ./

RUN mvn clean package

FROM openjdk:17-slim

COPY --from=MAVEN_BUILD /target/bloknot-parser-0.0.1-SNAPSHOT.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]
FROM maven:3.8.1-openjdk-17-slim as MAVEN_BUILD
WORKDIR /app-build
COPY . .
RUN mvn clean package

FROM openjdk:17-slim
WORKDIR /app
COPY --from=MAVEN_BUILD /app-build/target/bloknot-parser-0.0.1-SNAPSHOT.jar ./app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]

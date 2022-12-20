package com.example.bloknotparser.models;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "people")
public class Person {
	
	@Id
	private String id;
	
	private String firstname;
	
	private String lastname;
	
	private String patronymic;
	
	private String position;
	
	private String organization;
	
	public Person(String firstname, String lastname, String patronymic, String position, String organization) {
		this.firstname = firstname;
		this.lastname = lastname;
		this.patronymic = patronymic;
		this.position = position;
		this.organization = organization;
	}
}

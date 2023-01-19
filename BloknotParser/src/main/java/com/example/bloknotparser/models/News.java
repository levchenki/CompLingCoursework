package com.example.bloknotparser.models;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDateTime;

@Data
@Document(collection = "news")
public class News {
	
	@Id
	private String id;
	
	@Indexed(unique = true)
	private String title;
	
	private LocalDateTime date;
	
	private String link;
	
	private String text;
	
	@Field(name = "persons")
	private String persons;
	
	@Field(name = "places")
	private String places;
	
	public News(String title, LocalDateTime date, String link, String text) {
		this.title = title;
		this.date = date;
		this.link = link;
		this.text = text;
	}
}

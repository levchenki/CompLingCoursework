package com.example.bloknotparser.models;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

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
	
	private int commentsCount;
	
	public News(String title, LocalDateTime date, String link, String text, int commentsCount) {
		this.title = title;
		this.date = date;
		this.link = link;
		this.text = text;
		this.commentsCount = commentsCount;
	}
}

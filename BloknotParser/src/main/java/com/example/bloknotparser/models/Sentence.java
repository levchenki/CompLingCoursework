package com.example.bloknotparser.models;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "sentences")
public class Sentence {
	
	@Id
	private String id;
	
	private String detected;
	
	private String link;
	
	private String sentence;
	
	private String title;
	
	private String tonality;
	
	private String type;
}

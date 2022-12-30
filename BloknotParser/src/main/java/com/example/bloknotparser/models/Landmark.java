package com.example.bloknotparser.models;

import lombok.Data;
import org.checkerframework.common.aliasing.qual.Unique;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "landmarks")
public class Landmark {
	
	@Id
	private String id;
	
	@Unique
	private String name;
	
	public Landmark(String name){
		this.name = name;
	}
}

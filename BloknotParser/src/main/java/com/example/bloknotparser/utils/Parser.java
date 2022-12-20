package com.example.bloknotparser.utils;

import com.example.bloknotparser.repositories.NewsRepository;
import lombok.Data;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import java.io.IOException;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

@Data
public class Parser {
	
	private final String link;
	private NewsRepository newsRepository;
	private Document document;
	
	public Parser(String link) {
		this.link = link;
		try {
			while (document == null)
				this.document = Jsoup.connect(link).get();
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}
	
	public static LocalDateTime StringToDate(String str) {
		DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd.MM.yyyy");
		
		LocalTime time = LocalTime.of(3, 0);
		LocalDate now = LocalDate.now();
		
		if (str.contains("сегодня")) {
			return LocalDateTime.of(LocalDate.from(now), time);
		} else if (str.contains("вчера")) {
			return LocalDateTime.of(LocalDate.from(now.minusDays(1)), time);
		} else {
			return LocalDateTime.of(LocalDate.parse(str, formatter), time);
		}
		
	}
	
	public Document connect() {
		try {
			return Jsoup.connect(link).get();
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}
}

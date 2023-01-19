package com.example.bloknotparser.controllers;

import com.example.bloknotparser.models.Sentence;
import com.example.bloknotparser.services.SentenceService;
import lombok.AllArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/sentences")
public class SentencesController {
	
	private final SentenceService sentenceService;
	
	@GetMapping
	public List<Sentence> getAllSentences(
			@RequestParam(defaultValue = "0") int page,
			@RequestParam(defaultValue = "20") int size
	) {
		Pageable pageable = PageRequest.of(page, size);
		
		return sentenceService.getAllSentences(pageable).getContent();
	}
}

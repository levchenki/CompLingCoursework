package com.example.bloknotparser.services;

import com.example.bloknotparser.models.Sentence;
import com.example.bloknotparser.repositories.SentenceRepository;
import lombok.AllArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@AllArgsConstructor
@Transactional(readOnly = true)
public class SentenceService {
	
	private final SentenceRepository sentenceRepository;
	
	public Page<Sentence> getAllSentences(Pageable pageable) {
		return sentenceRepository.findAll(pageable);
	}
}

package com.example.bloknotparser.repositories;

import com.example.bloknotparser.models.News;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface NewsRepository extends MongoRepository<News, String> {
	Optional<News> findByTitle(String title);
	
	Optional<News> findById(String id);
	
	Page<News> findAllByOrderByDateDesc(Pageable pageable);
	
	void removeNewsByText(String text);
}

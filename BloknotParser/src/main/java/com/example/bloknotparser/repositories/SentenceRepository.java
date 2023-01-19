package com.example.bloknotparser.repositories;

import com.example.bloknotparser.models.Sentence;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface SentenceRepository extends MongoRepository<Sentence, String> {
}

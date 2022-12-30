package com.example.bloknotparser.repositories;

import com.example.bloknotparser.models.Landmark;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface LandmarkRepository extends MongoRepository<Landmark, String> {
	public Optional<Landmark> findLandmarkByName(String name);
}

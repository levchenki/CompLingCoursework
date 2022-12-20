package com.example.bloknotparser.repositories;

import com.example.bloknotparser.models.Person;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface PeopleRepository extends MongoRepository<Person, String> {
	
	Optional<Person> findPeopleByFirstnameAndLastnameAndPatronymic(String firstname, String lastname, String patronymic);
	
	Page<Person> findAllByOrderByLastnameAsc(Pageable pageable);
}

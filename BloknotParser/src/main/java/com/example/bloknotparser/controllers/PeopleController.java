package com.example.bloknotparser.controllers;

import com.example.bloknotparser.models.Person;
import com.example.bloknotparser.services.PeopleService;
import lombok.AllArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/people")
public class PeopleController {
	private final PeopleService peopleService;
	
	@GetMapping
	public List<Person> getAllPeople(
			@RequestParam(defaultValue = "0") int page,
			@RequestParam(defaultValue = "20") int size
	) {
		
		Pageable pageable = PageRequest.of(page, size);
		Page<Person> p = peopleService.getAllPeople(pageable);
		return p.getContent();
	}
	
	
	@PostMapping
	public void parsePeople() {
		peopleService.parse();
	}
	
}

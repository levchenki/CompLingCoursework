package com.example.bloknotparser.services;

import com.example.bloknotparser.models.Person;
import com.example.bloknotparser.repositories.PeopleRepository;
import com.example.bloknotparser.utils.Parser;
import lombok.AllArgsConstructor;
import org.jsoup.nodes.Document;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

@Service
@AllArgsConstructor
@Transactional(readOnly = true)
public class PeopleService {
	
	private final PeopleRepository peopleRepository;
	
	public Page<Person> getAllPeople(Pageable pageable) {
		return peopleRepository.findAllByOrderByLastnameAsc(pageable);
	}
	
	public void parse() {
		String link = "https://global-volgograd.ru/person";
		String param = "?offset=";
		
		for (int offset = 0; offset <= 200; offset += 20) {
			Parser parser = new Parser(link + param + offset);
			Document document = parser.getDocument();
			parsePage(document);
			System.out.println("Count: " + peopleRepository.count());
		}
	}
	
	private void parsePage(Document document) {
		var elements = document.getElementsByClass("person-block");
		ExecutorService executorService = Executors.newFixedThreadPool(elements.size());
		
		for (var el: elements) {
			executorService.submit(() -> {
				var fullName = el.getElementsByClass("title").get(0).text();
				var arr = fullName.split(" ");
				String lastname = arr[0].charAt(0) + arr[0].substring(1).toLowerCase();
				String firstname = arr[1];
				String patronymic = arr.length > 2 ? arr[2] : "";
				var position = el.getElementsByClass("person-text-position").get(0).text();
				
				var organization = el.getElementsByClass("person-text-org").select("a").attr("title");
				
				Person person = new Person(firstname, lastname, patronymic, position, organization);
				
				peopleRepository.findPeopleByFirstnameAndLastnameAndPatronymic(firstname, lastname, patronymic).ifPresentOrElse(
						(p) -> System.out.println("Человек уже существует"),
						() -> peopleRepository.save(person)
				);
				
			});
		}
		executorService.shutdown();
		try {
			executorService.awaitTermination(1, TimeUnit.HOURS);
		} catch (InterruptedException e) {
			throw new RuntimeException(e);
		}
	}
}

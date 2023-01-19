package com.example.bloknotparser.controllers;

import com.example.bloknotparser.models.News;
import com.example.bloknotparser.services.NewsService;
import lombok.AllArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/news")
public class NewsController {
	
	private final NewsService newsService;
	
	@GetMapping
	public List<News> getAllNews(
			@RequestParam(defaultValue = "0") int page,
			@RequestParam(defaultValue = "100") int size
	) {
		Pageable pageable = PageRequest.of(page, size);
		Page<News> p = newsService.getAllNews(pageable);
		
		return p.getContent();
	}
	
	@GetMapping("/count")
	public Long getCountNews() {
		return newsService.getCount();
	}
	
	@PostMapping
	public void parseNews(
			@RequestParam(defaultValue = "1") int fromPage,
			@RequestParam(defaultValue = "9390") int toPage,
			@RequestParam(defaultValue = "false") boolean reactive
	) {
		if (reactive) {
			newsService.parseReactive(fromPage, toPage);
		} else {
			newsService.parse(fromPage, toPage);
		}
	}
	
	@DeleteMapping
	public void removeEmptyNews() {
		newsService.deleteEmptyNews();
	}
}

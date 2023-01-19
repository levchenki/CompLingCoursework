package com.example.bloknotparser.services;

import com.example.bloknotparser.models.News;
import com.example.bloknotparser.repositories.NewsRepository;
import com.example.bloknotparser.utils.Parser;
import lombok.AllArgsConstructor;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Flux;

import java.time.LocalDateTime;
import java.util.Objects;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

@Service
@AllArgsConstructor
@Transactional(readOnly = true)
public class NewsService {
	
	private final NewsRepository newsRepository;
	
	public Page<News> getAllNews(Pageable pageable) {
		
		return newsRepository.findAllByOrderByDateDesc(pageable);
	}
	
	public void parse(int fromPage, int toPage) {
		String bloknotLink = "https://bloknot-volgograd.ru";
		String param = "/?PAGEN_1=";
		
		for (int page = fromPage; page <= toPage; page++) {
			Parser parser = new Parser(bloknotLink + param + page);
			Document document = parser.getDocument();
			parsePage(document, bloknotLink);
			
			System.out.println("Iteration: " + page * 10);
		}
	}
	
	public void parseReactive(int fromPage, int toPage) {
		String bloknotLink = "https://bloknot-volgograd.ru";
		String param = "/?PAGEN_1=";
		
		long start = System.currentTimeMillis();
		System.out.println("Parsing is starting");
		
		ExecutorService executorService = Executors.newFixedThreadPool(10);
		
		for (int page = fromPage; page <= toPage; page++) {
			int currentPage = page;
			executorService.submit(() -> {
				Parser parser = new Parser(bloknotLink + param + currentPage);
				Document document = parser.getDocument();
				
				try {
					Thread.sleep(1500);
				} catch (InterruptedException e) {
					throw new RuntimeException(e);
				}
				
				parsePageReactive(document, bloknotLink);
				System.out.println("Iteration: " + currentPage * 10);
			});
		}
		executorService.shutdown();
		try {
			executorService.awaitTermination(1, TimeUnit.HOURS);
		} catch (InterruptedException e) {
			throw new RuntimeException(e);
		}
		long end = System.currentTimeMillis();
		System.out.println("Parsing is over. Time: " + (end - start) / 1000 + " seconds");
	}
	
	private void parsePageReactive(Document document, String link) {
		var elements = document.getElementsByClass("bigline").select("li");
		
		Flux<Element> elementFlux = Flux.fromIterable(elements);
		
		elementFlux
				.take(elements.size())
				.subscribe(element -> {
					var anchor = element.getElementsByClass("sys");
					var title = anchor.text();
					var href = link + anchor.attr("href");
					int commentsCount = 0;
					
					var savedNews = newsRepository.findByTitle(title);
					
					savedNews.ifPresentOrElse(newsRepository::save, () -> {
						var stringDate = element.getElementsByClass("botinfo").get(0).text();
						LocalDateTime date = Parser.StringToDate(stringDate);
						String text = parseOneNews(href);
						News news = new News(title, date, href, text);
						newsRepository.save(news);
					});
				});
		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {
			throw new RuntimeException(e);
		}
	}
	
	private void parsePage(Document document, String link) {
		
		var elements = document.getElementsByClass("bigline").select("li");
		ExecutorService executorService = Executors.newFixedThreadPool(10);
		
		for (var el: elements) {
			executorService.submit(() -> {
				var anchor = el.getElementsByClass("sys");
				var href = link + anchor.attr("href");
				var title = anchor.text();
				int commentsCount = 0;
				
				var savedNews = newsRepository.findByTitle(title);
				
				savedNews.ifPresentOrElse((n) -> {
					newsRepository.save(n);
					System.out.print("u ");
				}, () -> {
					var stringDate = el.getElementsByClass("botinfo").get(0).text();
					LocalDateTime date = Parser.StringToDate(stringDate);
					String text = parseOneNews(href);
					News news = new News(title, date, href, text);
					newsRepository.save(news);
					System.out.print("s ");
				});
			});
		}
		executorService.shutdown();
		try {
			executorService.awaitTermination(1, TimeUnit.HOURS);
		} catch (InterruptedException e) {
			throw new RuntimeException(e);
		}
		
	}
	
	private String parseOneNews(String href) {
		Document newPageDocument = new Parser(href).connect();
		newPageDocument.getElementsByClass("news-picture").remove();
		
		var newsText = newPageDocument.getElementById("news-text");
		
		if (newsText == null)
			return "";
		
		newsText.getElementsByClass("hideme").remove();
		newsText.select("iframe").remove();
		Objects.requireNonNull(newsText.getElementById("strlen")).remove();
		String stringsToReplace = "((Реклама\\. ООО [\"«]Реклама Волгоград[\"»]\\. www.bloknot-volgograd\\.ru$)|([A-ЯЁ][а-яё]+\\s[A-ЯЁ][а-яё]+$))";
		
		return newsText.text().replaceAll(stringsToReplace, "");
	}
	
	
	public void deleteEmptyNews() {
		newsRepository.removeNewsByText("");
	}
	
}

package com.example.bloknotparser.services;

import com.example.bloknotparser.models.Landmark;
import com.example.bloknotparser.repositories.LandmarkRepository;
import lombok.AllArgsConstructor;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@AllArgsConstructor
@Transactional(readOnly = true)
public class LandmarkService {
	
	LandmarkRepository landmarkRepository;
	
	public void parse() {
		System.setProperty("webdriver.chrome.driver", "BloknotParser\\selenium\\chromedriver.exe");
		WebDriver webDriver = new ChromeDriver();
		String url = "https://avolgograd.com/sights?obl=vgg";
		webDriver.get(url);
		
		WebElement loadMoreButton = webDriver.findElement(By.xpath("//*[@id=\"true-loadmore\"]"));
		
		loadMoreButton.click();
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
			throw new RuntimeException(e);
		}
		
		List<WebElement> landmarkPost = webDriver.findElements(By.className("ta-211"));
		for (var post: landmarkPost) {
			String name = post.getText();
			
			if (findLandmarkByName(name).isEmpty()) {
				if (!name.equals("Память")) {
					Landmark landmark = new Landmark(name);
					landmarkRepository.save(landmark);
				}
			}
		}
		webDriver.quit();
	}
	
	public Optional<Landmark> findLandmarkByName(String name) {
		return landmarkRepository.findLandmarkByName(name);
	}
	
	public void deleteAllLandmarks() {
		landmarkRepository.deleteAll();
	}
	
	public Page<Landmark> getAllLandmarks(Pageable pageable) {
		return landmarkRepository.findAll(pageable);
	}
}


package com.example.bloknotparser.controllers;

import com.example.bloknotparser.models.Landmark;
import com.example.bloknotparser.services.LandmarkService;
import lombok.AllArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("landmarks")
public class LandmarkController {
	
	private final LandmarkService landmarkService;
	
	@GetMapping
	public List<Landmark> getAllLandmarks(
			@RequestParam(defaultValue = "0") int page,
			@RequestParam(defaultValue = "10") int size
	) {
		Pageable pageable = PageRequest.of(page, size);
		Page<Landmark> p = landmarkService.getAllLandmarks(pageable);
		return p.getContent();
	}
	
	@PostMapping
	public void parseLandmarks() {
		landmarkService.parse();
	}
	
	@DeleteMapping
	public void deleteLandmarks() {
		landmarkService.deleteAllLandmarks();
	}
}

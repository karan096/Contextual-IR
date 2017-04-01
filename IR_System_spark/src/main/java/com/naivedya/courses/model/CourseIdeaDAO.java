package com.naivedya.courses.model;

import java.util.List;

/**
 * Created by naivedya on 30/3/17.
 */
public interface CourseIdeaDAO {
    boolean add(CourseIdea idea);
    List<CourseIdea> findAll();
}

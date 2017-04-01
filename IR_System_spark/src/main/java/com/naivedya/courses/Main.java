package com.naivedya.courses;
import com.naivedya.courses.model.CourseIdea;
import com.naivedya.courses.model.CourseIdeaDAO;
import com.naivedya.courses.model.SimpleCourseIdeaDAO;
import spark.ModelAndView;
import spark.template.handlebars.HandlebarsTemplateEngine;

import java.util.HashMap;
import java.util.Map;

import static spark.Spark.*;

/**
 * Created by naivedya on 29/3/17.
 */
public class Main {
    public static void main(String[] args) {
        staticFileLocation("/public");
        CourseIdeaDAO dao = new SimpleCourseIdeaDAO();

        before((req, res) -> {
            if(req.cookie("username") != null) {
                req.attribute("username", req.cookie("username"));
            }
        });
        //TODO:nb - send message about redirect
        before("/ideas", (req, res) -> {
            if(req.attribute("username") == null)
            {
                res.redirect("/");
                halt();
            }
        });

        get("/", (req, res) -> {
            Map<String, String> model = new HashMap<>();
            //System.out.println(res.attribute("username"));
            model.put("username", req.attribute("username"));
            return new ModelAndView(model, "index.hbs");
        }, new HandlebarsTemplateEngine());

        post("/sign-in", (req, res) -> {
            Map<String, String> model = new HashMap<>();
            String username = req.queryParams("username");
            res.cookie("username", username);
            model.put("username", username);
            res.redirect("/");
            return null;
            //return new ModelAndView(model, "index.hbs");
        });

        get("/ideas", (req, res) -> {
            Map<String, Object> model = new HashMap<>();
            model.put("ideas", dao.findAll());
            return new ModelAndView(model, "ideas.hbs");
        }, new HandlebarsTemplateEngine());

        post("/ideas", (req, res)-> {
            String title = req.queryParams("title");
            // TODO:nb - username tied to cookie implementation
            CourseIdea courseIdea = new CourseIdea(title, req.attribute("username"));
            dao.add(courseIdea);
            res.redirect("/ideas");
            return null;
        });
        //get("/hello", (req, res) -> "Hello World");
    }
}

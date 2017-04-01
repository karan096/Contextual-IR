package com.naivedya.courses;
import spark.ModelAndView;
import spark.Request;
import spark.Response;
import spark.template.handlebars.HandlebarsTemplateEngine;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static spark.Spark.*;

/**
 * Created by naivedya on 30/3/17.
 */
public class Search {
    public static void main(String[] args) {
        staticFileLocation("/public");
        get("/", (req, res) -> {
            return new ModelAndView(null, "home.hbs");
        }, new HandlebarsTemplateEngine());

        post("/Search", (Request req, Response res) -> {
            String query = req.queryParams("query");
            System.out.println(query);
            SearchFiles sc=new SearchFiles();
            List<String> results=sc.search(query);
            Map<String, Object> model = new HashMap<>();
            model.put("results", results);
            return new ModelAndView(model, "results.hbs");
        }, new HandlebarsTemplateEngine());
    }
}

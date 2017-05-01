package com.naivedya.ir_system;
import javafx.util.Pair;
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
        get("/hello", (req, res) -> "Hello World");

        get("/", (req, res) -> {
            return new ModelAndView(null, "home.hbs");
        }, new HandlebarsTemplateEngine());

        post("/Search", (Request req, Response res) -> {
            String query = req.queryParams("query");
            System.out.println(query);
            SearchFiles sc=new SearchFiles();
            MySpellChecker spellChecker = new MySpellChecker("/home/naivedya/IdeaProjects/ir_system/src/main/resources/public/dictionary/corncob_lowercase.txt");
            String correction = spellChecker.doCorrection(query);
            if(query.equalsIgnoreCase(correction))
                correction = "";
            List<Pair<String, String>> results=sc.search(query);
            Map<String, Object> model = new HashMap<>();
            model.put("correction", correction);
            model.put("results", results);
            model.put("count", results.size());
            model.put("query", query);
            return new ModelAndView(model, "results_styled.hbs");
        }, new HandlebarsTemplateEngine());

    }
}

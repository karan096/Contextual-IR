package com.naivedya.courses;


import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class SearchFiles {

    public SearchFiles() {
    }

    public static void main(String[] args) throws Exception {
        String usage =
                "Usage:\tjava org.apache.lucene.demo.SearchFiles [-index dir] [-field f] [-repeat n] [-queries file] [-query string] [-raw] [-paging hitsPerPage]\n\nSee http://lucene.apache.org/core/4_1_0/demo/ for details.";
        if (args.length > 0 && ("-h".equals(args[0]) || "-help".equals(args[0]))) {
            System.out.println(usage);
            System.exit(0);
        }
    }

    public List<String> search(String s) throws Exception {
        String index = "/home/naivedya/IdeaProjects/course-ideas/src/main/resources/public/index";
        String field = "contents";
        String queries = null;
        boolean raw = false;

        String queryString = s;


        int hitsPerPage = 100;
        IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(index)));
        IndexSearcher searcher = new IndexSearcher(reader);
        Analyzer analyzer = new StandardAnalyzer();

        BufferedReader in = null;
        QueryParser parser = new QueryParser(field, analyzer);

        Query query = parser.parse(queryString);

        System.out.println("Searching for: " + query.toString(field));
        searcher.search(query, null, 100);
        List<String> li = doSearch(in, searcher, query, hitsPerPage, raw, queries == null && queryString == null);
        reader.close();
        return li;
    }

    public List<String> doSearch(BufferedReader in, IndexSearcher searcher, Query query,
                                 int hitsPerPage, boolean raw, boolean interactive) throws IOException {
        TopDocs results = searcher.search(query, 5 * hitsPerPage);
        ScoreDoc[] hits = results.scoreDocs;
        int numTotalHits = results.totalHits;
        System.out.println(numTotalHits + " total matching documents");
        int start = 0;
        int end = Math.min(numTotalHits, hitsPerPage);
        List<String> li = new ArrayList<>();
        for (int i = start; i < end; i++) {
            Document doc = searcher.doc(hits[i].doc);
            String path = doc.get("path");

            File f = new File(path);
            System.out.println(f.getName());

            if (path != null) {
                //System.out.println((i + 1) + ". " + path);
                int ind = path.indexOf("testdata");
                path = path.substring(ind);
                li.add(path);
                String title = doc.get("title");
                if (title != null) {
                    System.out.println("   Title: " + doc.get("title"));
                }
            } else {
                System.out.println((i + 1) + ". " + "No path for this document");
            }
        }
        return li;
    }
}

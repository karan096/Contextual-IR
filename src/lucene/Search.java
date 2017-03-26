package lucene;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.*;
import java.io.*;
import java.util.*;  

/**
 * Servlet implementation class Search
 */
@WebServlet("/Search")
public class Search extends HttpServlet {
	
	public void service(HttpServletRequest req ,HttpServletResponse res)throws ServletException,IOException
	{
		String que=req.getParameter("query");
		
		SearchFiles sc=new SearchFiles();
		try{
			String[] results=sc.search(que);
			PrintWriter out=res.getWriter();
			out.println(results[0]);
		}
		catch(Exception e){
			
		}
	}
}

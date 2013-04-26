import play.*;
import play.Application;
import play.libs.F.Promise;
import play.libs.WS;
import play.libs.WS.Response;

public class Global extends GlobalSettings {

  @Override
  public void onStart(Application app) {
    Logger.info("Application has started");
   Promise<Response> response =  WS.url("https://api.twitter.com/oauth2/token")
    .setHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8")
    .setHeader("Authorization", "Basic aTh4U05GUlB6UDlQMFcwODFJMDQ5UToxa0RMbFYyZTc0cWtPY3V5NEJTU1BZQTh3YnllTDJyMEtPZzVBZzhv")
    .post("grant_type=client_credentials");
   
   Logger.info("response: " + response.get().getBody());
    
    Promise<Response> response2 =  WS.url("https://api.twitter.com/1.1/statuses/user_timeline.json")
   .setHeader("Authorization", "Bearer AAAAAAAAAAAAAAAAAAAAAOkUQgAAAAAA9bzlYuX3WxYe2XJWNq2Jb9h5sME%3DwT0AeQkNAkAJuRjG0Hx3ynjFU8VFoJ7LGnhsSqmVZsE")
   .setQueryParameter("screen_name", "BarebakAssassin")
   .get();
    
    Logger.info("response2: " + response2.get().getBody());
    
    Logger.info("text: " + response2.get().asJson().findValues("text").get(0).asText());

   
  }  

  @Override
  public void onStop(Application app) {
    Logger.info("Application shutdown...");
  }  
}
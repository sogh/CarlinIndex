package models;

import javax.persistence.*;
import play.db.ebean.*;
import com.avaje.ebean.*;

@Entity
public class User extends Model {

    @Id
    public String name;
    public double carlinIndex;
    public String topTweet;
    
    public User(String name, double carlinIndex, String topTweet) {
      this.name = name;
      this.carlinIndex = carlinIndex;
      this.topTweet = topTweet;
    }

    public static Finder<String,User> find = new Finder<String,User>(
        String.class, User.class
    ); 
}
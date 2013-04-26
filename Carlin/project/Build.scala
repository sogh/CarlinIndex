import sbt._
import Keys._
import play.Project._

object ApplicationBuild extends Build {

  val appName         = "Carlin"
  val appVersion      = "1.0-SNAPSHOT"

  val appDependencies = Seq(
    // Add your project dependencies here,
    javaCore,
    javaJdbc,
    javaEbean,
    "org.webjars" % "webjars-play" % "2.1.0-1",
    "org.webjars" % "bootstrap" % "2.1.1",
    "mysql" % "mysql-connector-java" % "5.1.18"
  )

  val main = play.Project(appName, appVersion, appDependencies).settings(
    // Add your own project settings here      
    resolvers += "webjars" at "http://webjars.github.com/m2"
  )

}

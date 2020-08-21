$(document).ready(function(){
    $(window).on("popstate", function(){
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
    $(".to_uKit").on("click", function(){
      history.pushState("", "", "/urgency");
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
    $(".to_robbery").on("click", function(){
      history.pushState("", "", "/robbery");
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
    $(".to_health").on("click", function(){
      history.pushState("", "", "/health");
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
    $(".to_hunger").on("click", function(){
      history.pushState("", "", "/hunger");
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
    $(".to_home").on("click", function(){
      history.pushState("", "", "/");
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
    $(".to_profile").on("click", function(){
      history.pushState("", "", "/profile");
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
    $(".to_notifications").on("click", function(){
      history.pushState("", "", "/notifications");
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
    $(".to_dashboard").on("click", function(){
      history.pushState("", "", "/dashboard");
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
    $(".to_announcement").on("click", function(){
      history.pushState("", "", "/announcement");
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
    $(".to_login").on("click", function(){
      history.pushState("", "", "/login");
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
    $(".to_register").on("click", function(){
      history.pushState("", "", "/register");
      $("#body").load(location.href + "#body");
      $("#body").load(location.href + "#navbar");
    });
});
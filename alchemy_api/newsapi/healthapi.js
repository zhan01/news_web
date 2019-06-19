
$(document).ready(function(){

    let url = "https://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=31e6e9bf91a24a4d9fc8da17bb849d34";
        
        $.ajax({
            url: url,
            method: "GET",
            dataType: "json",

            beforeSend: function(){
                $(".progress").show();
            },

            complete: function(){
                $(".progress").hide();
            },

            success: function(news){
                let output = "";
                let latestNews = news.articles;
                
                for(var i in latestNews){
                    output +=`

                        <div class="col l6 m6 s12">
                            
                                <h4>${latestNews[i].title}</h4>
                                <div class="card-image">
                                    <img src="${latestNews[i].urlToImage}" class="responsive-img">
                                </div>
                                
                                <p>${latestNews[i].descripton}</p>
                                <p>${latestNews[i].content}</p>
                                <p>Published on: ${latestNews[i].publishedAt}</p>
                                <a href="${latestNews[i].url}" class="btn">Read more</a>
                                
                            
                        </div>
                    
                    `;
                }

                if(output != ""){

                    $("#newsResult").html(output);

                }else{
                    let NewsnotFound = "This news isn't available. Sorry about that. Try search for something else";
                    $("#newsResult").html(NewsnotFound);
                }
            },

            error: function(){
                console.log("error");
            }

        });
   
});
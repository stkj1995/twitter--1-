from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import x 
import time
import uuid
import os

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)

# Set the maximum file size to 10 MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024   # 1 MB

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
 

##############################
##############################
##############################
def _____USER_____(): pass 
##############################
##############################
##############################

@app.get("/")
def view_index():
   
    return render_template("index.html")

##############################
@app.get("/login")
def view_login():
    if session.get("user", ""): return redirect(url_for("view_home"))

    message = request.args.get("message", "")
    return render_template("login.html", message=message)

##############################
@app.post("/login")
def handle_login():
    try:
        # Validate
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        # Connect to the database
        q = "SELECT * FROM users WHERE user_email = %s"
        db, cursor = x.db()
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        if not user: raise Exception("User not found", 400)

        if not check_password_hash(user["user_password"], user_password):
            raise Exception("Invalid credentials", 400)

        user.pop("user_password")

        session["user"] = user
        return redirect(url_for("view_home"))

    except Exception as ex:
        ic(ex)
        if ex.args[1] == 400: return redirect(url_for("view_login", message=ex.args[0]))
        return "System under maintenance", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/signup")
def view_signup():
    message = request.args.get("message", "")
    return render_template("signup.html", message=message)

##############################
@app.post("/signup")
def handle_signup():
    try:
        # Validate
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()

        user_hashed_password = generate_password_hash(user_password)

        # Connect to the database
        q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s)"
        db, cursor = x.db()
        cursor.execute(q, (None, user_email, user_hashed_password, user_username, user_first_name))
        db.commit()
        return redirect(url_for("view_login", message="Signup successful. Proceed to login"))
    except Exception as ex:
        ic(ex)
        if ex.args[1] == 400: return redirect(url_for("view_signup", message=ex.args[0]))
        if "Duplicate entry" and user_email in str(ex): return redirect(url_for("view_signup", message="Email already registered"))
        if "Duplicate entry" and user_username in str(ex): return redirect(url_for("view_signup", message="username already registered"))
        return "System under maintenance", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/home")
@x.no_cache
def view_home():
    try:
        #user = session.get("user", "")
        # if not user: return redirect(url_for("view_login"))
        db, cursor = x.db()
        # Follow suggestions
        q_follow = "SELECT * FROM follow_suggestions ORDER BY created_at DESC LIMIT 5"
        cursor.execute(q_follow)
        follow_suggestions = cursor.fetchall()
        
        # Trends
        q_trends = "SELECT * FROM trends ORDER BY created_at DESC LIMIT 5"
        cursor.execute(q_trends)
        trends = cursor.fetchall()
        
        # Tweets
        q_tweet = "SELECT * FROM posts ORDER BY post_pk DESC LIMIT 10"
        cursor.execute(q_tweet)
        tweet = cursor.fetchall()

        # Posts
        q_posts = "SELECT * FROM users JOIN posts ON user_pk = post_user_fk ORDER BY RAND() LIMIT 10"
        cursor.execute(q_posts)
        rows = cursor.fetchall()
        
        # Hearts / likes
        q_heart = "SELECT * FROM posts ORDER BY post_total_likes DESC LIMIT 10"
        cursor.execute(q_heart)
        heart = cursor.fetchall()
        
        return render_template(
            "home.html",
            follow_suggestions=follow_suggestions,
            trends=trends,
            tweet=tweet,
            heart=heart,
            rows=rows,
        )
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



##############################
@app.get("/logout")
def handle_logout():
    try:
        session.clear()
        return redirect(url_for("view_login"))
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass

##############################
@app.get("/ajax")
def ajax():
    try:
       return render_template("ajax.html")
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass

##############################
@app.get("/tweet")
def api_tweet():
    try:
       return "You did it"
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass

##############################
@app.get("/ajax-post")
def view_ajax_post():
    try:
       return render_template("ajax_post.html")
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass

    
##############################
@app.post("/save")
def api_save():
    try:
       user_name = request.form.get("user_name", "")
       user_last_name = request.form.get("user_last_name", "")
       user_nickname = request.form.get("user_nickname", "")

        ## Dictionary in Python is JSON in Javascript
       user = {
        "user_name" : user_name.title(),
        "user_last_name" : user_last_name.title(),
        "user_nickname" : user_nickname.title()
        }

       return user
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass



##############################
@app.get("/ajax-heart")
def view_ajax_heart():
    try:
       return render_template("ajax_heart.html")
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass

##############################
@app.get("/api-like-tweet")
def api_like_tweet():
    try:
       # Validate the data
       # Get the logged user id
       # Connect to the database
       # Disconnect from the database
       # Insert the liking of a tweet in the table
       # Check that everything went as expected
       # Reply to the browser information that the tweet is liked

       return {"status":"OK"}
    except Exception as ex:
        ic(ex)
        return {"status":"error"}
    finally:
        pass

##############################
@app.get("/api-unlike-tweet")
def api_unlike_tweet():
    try:
       # Validate the data
       # Get the logged user id
       # Connect to the database
       # Disconnect from the database
       # Delete the liking of a tweet in the table
       # Check that everything went as expected
       # Reply to the browser information that the tweet is liked

       return {"status":"OK"}
    except Exception as ex:
        ic(ex)
        return {"status":"error"}
    finally:
        pass


##############################
@app.get("/ajax-bookmark")
def view_ajax_bookmark():
    try:
       return render_template("ajax_bookmark.html")
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass

##############################
@app.post("/api-bookmark")
def api_bookmark():
    try:
       return """
        <mixhtml mix-replace='button'>
            <button mix-post="/api-remove-bookmark">
                 <i class="fa-solid fa-bookmark"></i>
            </button>
        </mixhtml>
        <mixhtml mix-top="button">
            <div mix-ttl="5000" mix-fade-out>I will disappear</div>
        </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass


##############################
@app.get("/items")
def view_items():
    try:
       db, cursor = x.db()
       q = "SELECT * FROM posts LIMIT 0, 2"
       cursor.execute(q)
       items = cursor.fetchall()
       ic(items)
       return render_template("items.html", items=items)
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/api-get-items")
def api_get_items():
    try:
        next_page = int(request.args.get("page", "")) # 2
        ic(next_page)
        db, cursor = x.db()
        q = "SELECT * FROM posts LIMIT %s, 2"
        cursor.execute(q, (next_page,))
        items = cursor.fetchall()        
        ic(items)
        container = ""

        for item in items:
            html_item = render_template("_item.html", item=item)
            container = container + html_item
        ic(container)

        return f"""
        <mixhtml mix-bottom="#items">
        {container}
        </mixhtml>
        """
    
    
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        if "cursor" in locals(): cursor.close()    
        if "db" in locals(): db.close()    

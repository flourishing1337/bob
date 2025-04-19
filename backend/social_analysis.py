import instaloader

def get_instagram_data(username):
    L = instaloader.Instaloader()

    profile = instaloader.Profile.from_username(L.context, username)
    
    return {
        "username": username,
        "followers": profile.followers,
        "following": profile.followees,
        "posts_count": profile.mediacount,
        "bio": profile.biography,
        "external_url": profile.external_url
    }

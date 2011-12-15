from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from friendship.models import Friend, Follow, FriendshipRequest


def view_friends(request, username, template_name='friendship/friends_list.html'):
    """ View the friends of a user """
    user = get_object_or_404(User, username=username)
    friends = Friend.objects.friends(user)

    return render(request, template_name, {'user': user, 'friends': friends})


@login_required
def add_friend(request, to_username, template_name='friendship/friends_add.html'):
    """ Create a FriendshipRequest """
    if request.POST:
        to_user = User.objects.get(username=to_username)
        from_user = request.user
        Friend.objects.add_friend(from_user, to_user)
        return redirect('friendship_requests')

    return render(request, template_name, {'to_username': to_username})


@login_required
def accept_friend(request, friendship_request_id):
    """ Accept a friendship request """
    if request.POST:
        f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
        f_request.accept()
        return redirect('friendship_view_friends', username=request.user.username)

    return redirect('friendship_request_detail', friendship_request_id=friendship_request_id)


@login_required
def reject_friend(request, friendship_request_id):
    """ Reject a friendship request """
    if request.POST:
        f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
        f_request.reject()
        return redirect('friendship_requests')

    return redirect('friendship_request_detail', friendship_request_id=friendship_request_id)


@login_required
def cancel_friend(request, friendship_request_id):
    """ Cancel a previously created friendship_request_id """
    if request.POST:
        f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
        f_request.cancel()
        return redirect('friendship_requests')

    return redirect('friendship_request_detail', friendship_request_id=friendship_request_id)


@login_required
def friendship_request_list(request, template_name='friendship/friendship_requests_list.html'):
    """ View unread and read friendship requests """
    # friendship_requests = Friend.objects.requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)
    return render(request, template_name, {'requests': friendship_requests})


@login_required
def friendship_request_list_rejected(request, template_name='friendship/friendship_requests_list.html'):
    """ View rejected friendship requests """
    # friendship_requests = Friend.objects.rejected_requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)
    return render(request, template_name, {'requests': friendship_requests})


@login_required
def friendship_request(request, friendship_request_id, template_name='friendship/friendship_request.html'):
    """ View a particular friendship request """
    f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)

    return render(request, template_name, {'friendship_request': f_request})


def followers(request, username, template_name='friendship/followers_list.html'):
    """ List this user's followers """
    user = get_object_or_404(User, username=username)
    followers = Follow.objects.followers(user)

    return render(request, template_name, {'user': user, 'followers': followers})


def following(request, username, template_name='friendship/following_list.html'):
    """ List who this user follows """
    user = get_object_or_404(User, username=username)
    following = Follow.objects.following(user)

    return render(request, template_name, {'user': user, 'following': following})


@login_required
def add_follower(request, followee_username, template_name='friendship/following_add.html'):
    """ Create a following relationship """
    if request.POST:
        followee = User.objects.get(username=followee_username)
        follower = request.user
        Follow.objects.add_follower(follower, followee)
        return redirect('friendship_following', username=follower.username)

    return render(request, template_name, {'followee_username': followee_username})


@login_required
def remove_follower(request, followee):
    """ Remove a following relationship """
    pass


def all_users(request, template_name="friendship/user_actions.html"):
    users = User.objects.all()

    return render(request, template_name, {'users': users})
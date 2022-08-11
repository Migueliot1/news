
<div class="article__comments_answer_body">
            <div class="article__comment_user">
                <div class="acc__comment_user_left">
                    <img class="acc__comment_user_img" src="{{ comment.owner.profile_image.url }}" />
                    <div class="acc__comment_user_time">
                        <p class="acc__comment_username">{{ comment.owner.username }}</p>
                        <p class="acc__comment_time">{{ comment.created }}</p>
                    </div>
                </div>
                <div class="acc__comment_user_right">
                    <div class="acc__comment_vote">
                        <i class="bx bx-chevron-down" id="vote-down"></i>
                        <span>{{ comment.vote_total }}</span>
                        <i class="bx bx-chevron-up" id="vote-up"></i>
                    </div>
                </div>
            </div>
            <div class="article__comment_content">
                <div class="article__comment_text">
                    <p class="article__comment_text_comment">{{ comment.comment_body|linebreaksbr }}</p>
                </div>
                <div class="article__comment_answer">
                    <p class="article__comment_answer_btn">Answer</p>
                    {% if request.user.is_authenticated %}
                        {% if request.user == comment.owner.user %}
                            <a href="{% url 'delete_comment' comment.id %}" class="article__comment_delete_btn">Delete</a>
                        {% endif %}
                    {% endif %}
                </div>
            </div>
</div>
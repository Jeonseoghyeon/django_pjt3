# README

> 0422 Django Project 3 팀 프로젝트 1:N 데이터 기반으로 한 Accounts,Community Apps 구현

## 1. 프로젝트 시작

>팀프로젝트인 만큼  Project 시작이 개인프로젝트와 달랐습니다.
>
>협업 Tool은 Slack, Trello였습니다. 개발환경 : CS9

1. 프로젝트 시작

   ``` 
   django-admin startproject django_pjt3
   ```

2. settings.py 설정

   - ALLOWED_HOSTS = ['*']

   - locale 설정 : TZ

   - 'base.html' 적용을 위한 DIR 설정

     ```python
     'DIRS': [os.path.join(BASE_DIR,'templates')]
     ```

3. 앱 생성

   ```
   python manage.py startapp accounts
   python manage.py startapp community
   ```

4. INSTALLED_APPS에 앱 등록

5. urls.py에 app 경로 설정(include)

   ```python
   from django.contrib import admin
   from django.urls import path, include
   
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('accounts/', include('accounts.urls')),
       path('community/',include('community.urls')),
   ]
   ```



## 2. App 구현(어려웠던 점, 알게된 점 포함)

> 각 App 별로 Driver, Navigator 역할을 바꿔가며 진행했습니다.(라고 믿고싶습니다.)
>
> User가 먼저 DB에 있어야 이후 Review, Comment의 1:N DB 생성이 수월할 것이라고 판단하여 Accounts App 먼저 구현했습니다.

- ### 2-1. Accounts(Driver:전석현, Navigator:이창완)

  - `urls.py`

    - app_name은 app의 이름으로 설정해 주었습니다.

    - signup, login, logout에 해당하는 루트, 해당 루트에 들어오면 실행할 함수, urlnamespace까지 설정해 주었습니다.

    ```python
    from django.contrib import admin
    from django.urls import path
    from . import views
    
    app_name = 'accounts'
    urlpatterns = [
        path('',views.index,name='index'),
        path('signup/',views.signup,name='signup'),
        path('login/',views.login,name='login'),
        path('logout/',views.logout,name='logout')
        ]
    ```

  - `views.py`

    - index, signup, login, logout 4개의 함수를 구현해 주었습니다.
      - index 함수는 구현시 편의를 위해서만 작성했고, community앱 생성 후엔 쓰이지 않았습니다.
      - signin, login, logout 기능은 django내 form, method를 이용했습니다.
        - signin
          - `UserCreationForm`
        - login
          - `AuthenticationForm, auth_login`
        - logout
          - `auth_logout`
    - 어려웠던 부분은 `3. 어려웠던 점`에서 다룰 예정

    ```python
    from django.shortcuts import render,redirect,get_object_or_404
    from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
    from django.contrib.auth import login as auth_login
    from django.contrib.auth import logout as auth_logout
    from django.contrib.auth import authenticate
    from django.contrib.auth import get_user_model
    from django.contrib.auth.decorators import login_required
    
    # Create your views here.
    def index(request):
        return render(request, 'accounts/index.html')
    
    def signup(request):
        if request.user.is_authenticated:
            return redirect('community:review_list')
        else:
            if request.method == "POST":
                form = UserCreationForm(request.POST)
                if form.is_valid():
                    new_user=form.save()
                    authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
                    auth_login(request,authenticated_user)
                    return redirect('community:review_list')
            else:
                form = UserCreationForm()
            context = {
                'form':form
            }
            return render(request, 'accounts/signup.html',context)
    
    def login(request):
        if request.user.is_authenticated:
            return redirect('community:review_list')
        else:
            if request.method == "POST":
                form = AuthenticationForm(request,request.POST) # 
                if form.is_valid():
                    auth_login(request,form.get_user()) # AuthenticationForm 메서드
                    return redirect(request.GET.get('next') or 'community:review_list') #
            else:
                form = AuthenticationForm()
            context={
                'form':form
            }
            return render(request,'accounts/login.html',context)
    
    @login_required
    def logout(request):
        auth_logout(request)
        return redirect('community:review_list')
    ```

  - templates

    - `login.html`

      ```html
      {% extends 'base.html' %}
      {% block body %}
      
      <div class="mt-5 justify-content-center" style="border:1px solid black">
      
          <h1 class="text-center my-5">로 그 인</h1>
      <form action="" method="POST">
          {% csrf_token %}
          <div class="d-flex mx-auto my-5 justify-content-center">
              <div class="mx-5">사용자 이름 : </div> <div class="mx-5">{{ form.username}}</div>
          </div>
          <div class="d-flex mx-auto my-5 justify-content-center">
              <div class="mx-5">비밀 번호 :</div>   <div class="mx-5">{{ form.password}}</div>
          </div>
          <div class="d-flex justify-content-center">
          <button class="btn btn-primary px-5 my-5" type="submit">로그인</button>
          </div>
      </form>
      </div>
      
      
      {% endblock %}
      ```

      

    - `signup.html`

      ```html
      {% extends 'base.html' %}
      {% block body %}
      <div class="my-5" style="border:1px solid black">
          <div class="h1 text-center my-5">회원가입</div>
      <form action="" method="POST">
          {% csrf_token %}
          <div class="mx-5">{{ form.as_p }}
          </div>
              <div class="d-flex justify-content-center">
          <button class="btn btn-primary px-5 my-5" type="submit">회원가입</button>
          </div>
      </form>
      </div>
      {% endblock %}
      ```






- ### 2-2. Community (Driver:이창완, Navigator:전석현)

  - `urls.py`

    - app_name은 app의 이름으로 설정해 주었습니다.

    - signup, login, logout에 해당하는 루트, 해당 루트에 들어오면 실행할 함수, urlnamespace까지 설정해 주었습니다.

    ```python
    from django.urls import path
    from . import views
    app_name='community'
    
    urlpatterns=[
        path('',views.review_list,name='review_list'),
        path('create/',views.review_create,name='review_create'),
        path('<int:review_id>/',views.review_detail,name='review_detail'),
        path('<int:review_id>/delete/',views.review_delete,name='review_delete'),
        path('<int:review_id>/update/',views.review_update,name='review_update'),
        path('<int:review_id>/comments/',views.comments_create,name='comments_create'),
      path('<int:review_id>/comments/<int:comment_id>/delete',views.comments_delete,name='comments_delete'),
        ]
    ```

  - `views.py`

    - @login_required의 용도 : 어떤 기능을 할 때, login이 안되어있으면 로그인 창을 불러준다!
    - @require_POST의 용도 : POST 방식으로 오지 않으면 함수 작동 안시킴

    ```python
    from django.shortcuts import render,redirect,get_object_or_404
    from .forms import ReviewForm, CommentForm
    from .models import Review, Comment
    from django.contrib.auth.decorators import login_required
    from django.views.decorators.http import require_POST
    # Create your views here.
    def review_list(request):
        reviews=Review.objects.order_by('-id')
        context={
            'reviews':reviews
        }
        return render(request,'community/review_list.html',context)
    
    
    @login_required
    def review_create(request):
        if request.method == 'POST':
            form=ReviewForm(request.POST)
            if form.is_valid():
                review=form.save(commit=False)
                review.user=request.user
                review.save()
                return redirect('community:review_list')
        else:
            form=ReviewForm()
        context={
            'form':form
        }
        return render(request,'community/form.html',context)
    
    def review_detail(request,review_id):
        review=get_object_or_404(Review,id=review_id)
        form=CommentForm()
        context={
            'review':review,
            'form':form,
        }
        return render(request,'community/review_detail.html',context)
    
    @login_required
    def review_update(request,review_id):
        review=get_object_or_404(Review,pk=review_id)
        if request.user == review.user:
            if request.method=='POST':
                form = ReviewForm(request.POST,instance=review)
                if form.is_valid():
                    form.save()
                    return redirect('community:review_detail',review_id)
            else:
                form = ReviewForm(instance=review)
    
            context={
                'form':form
            }
            return render(request,'community/form.html',context)
        else:
            return redirect('community:review_detail',review_id)
    @require_POST
    @login_required
    def review_delete(request,review_id):
        if request.method=='POST':
            review = get_object_or_404(Review,pk=review_id)
            if request.user == review.user:
                review.delete()
                return redirect('community:review_list')
            else:
                return redirect('community:review_detail',review_id)
    
    
    @login_required
    def comments_create(request,review_id):
        review = get_object_or_404(Review, pk=review_id)
        if request.method=='POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.review = review
                comment.user=request.user
                comment.save()
        return redirect('community:review_detail',review_id)
    
    @login_required
    def comments_delete(request,review_id,comment_id):
        comment=get_object_or_404(Comment,id=comment_id)
        if request.user == comment.user:
            if request.method=='POST':
                comment.delete()
                return redirect('community:review_detail', review_id)
        else:
            return redirect('community:review_detail', review_id)
    ```

  - `models.py`

    - USER를 불러올 때!!! settings.AUTH_USER_MODEL을 해줬다!
      - 이부분 내가 아예 모르던 개념이었는데.. 팀원인 창완이형이 설명해주시면서 도와주심!
      - User class는 따로 선언해놓은 적이 없지만, Django 내의 자체 User Model을 사용하기 때문에 불러와준 것 뿐이다. 
    - User라는 1에 속한 Review라는 N을 구현하고, 또 그 N에 속하는 각각의 1에 Comment라는 N을 구현해 보았다.
      - Review는 창완이 형이, Comment는 내가 했는데 개념을 알고 접근하니 큰 어려움 없이(똑같은 방법으로) 구현해낼 수 있었다.
    - 오늘 프로젝트하면서 제일 많이 공부하게 된 부분(Model + ModelForm!)

    ```python
    from django.db import models
    from django.conf import settings
    # Create your models here.
    class Review(models.Model):
        title=models.CharField(max_length=100)
        movie_title=models.CharField(max_length=30)
        rank=models.IntegerField(default=0)
        content=models.TextField()
        created_at=models.DateTimeField(auto_now_add=True)
        updated_at=models.DateTimeField(auto_now=True)
        user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    class Comment(models.Model):
        user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
        review=models.ForeignKey(Review,on_delete=models.CASCADE)
        content=models.CharField(max_length=200)
        created_at=models.DateTimeField(auto_now_add=True)
        updated_at=models.DateTimeField(auto_now=True)
    
    ```

  - `forms.py`

    - 크게 다른건 없었지만, ReviewForm 내에서 widgets을 통해 꾸며주는 방법, 아래처럼 Class Meta 위에 각각의 속성을 꾸며주는 방법이 있다는 것을 알았다.
    - 이 부분에서 Bootsrap을 적용할 수 있다는 로직이 이해가 어려웠고, 지금도 100% 이해되진 않는다... __교수님이 나중에 수업때 말씀해주시면 좋겠다...__

    ```python
    from django import forms
    from .models import Review,Comment
    
    class ReviewForm(forms.ModelForm):
        title = forms.CharField(
                label='제목',
                help_text='',
                widget=forms.TextInput(
                        attrs={
                            'class': 'w-100 ',
                            'placeholder': '제목 입력'
                        }
                    )
            )
        content = forms.CharField(
                label='내용',
                help_text='자유롭게 작성해주세요.',
                widget=forms.Textarea(
                        attrs={
                            'class':'w-100',
                        }
                    )
            )
        movie_title = forms.CharField(
                label='영화제목',
                widget=forms.TextInput(
                        attrs={
                            'class':'w-100',
                        }
                    )
            )
        rank = forms.CharField(
                label='별점',
                widget=forms.NumberInput(
                        attrs={
                            'class':'w-100',
                            'max':'10',
                            'min':'0'}
                    )
            )
        class Meta:
            model=Review
            fields=['title','movie_title','rank','content']
    
    class CommentForm(forms.ModelForm):
        class Meta:
            model=Comment
            fields=['content',]
    
    
    ```

  - templates

    - `form.html`

      ```html
      {% extends 'base.html' %}
      
      {% block body %}
      
      
      {% if request.resolver_match.url_name == 'review_create' %} <!--이부분 공식문서 참고-->
          <div class="my-5 text-center h1">새글 쓰기</div>
      {% else %}
          <div class="my-5 text-center h1">글 수정하기</div>
      {% endif %}
      
      <form action="" method='POST'>
          {% csrf_token %}
          {{ form }}
      
          <button> 작성완료 </button>
      
      </form>
      
      {% endblock %}
      ```

    - `review_detail.html`

      ```html
      {% extends 'base.html' %}
      
      {% block body %}
      
      
          <div class="text-center h1 col-6 offset-3 mt-5 mb-5" style="border-bottom: 2px solid">영화 리뷰 게시판</div>
          <div class="row justify-content-center border">
              <div class="h4 text-center border-bottom col-8 offset-2 my-5 mx-0 px-0">{{ review.title }}</div>
              <div class="h4 text-center border-bottom col-8 offset-2 mb-5 mx-0 px-0">작성자 : {{ review.user }}</div>
              <p class="col-12 text-justify py-5 px-5 text-warning" style=" border:solid 1px black;font-size:1rem">
                  {{review.content}}
              </p>
              <div class="col-12 h4 text-center">
                  평점 : {{ review.rank }}
              </div>
      
              <div class="offset-4 col-8 text-right mt-5">
                 <p> 작성 날짜 : {{ review.created_at}} </p>
              </div>
              <div class="offset-4 col-8 text-right">
                 <p> 수정 날짜 : {{ review.updated_at}} </p>
              </div>
      
                  {% if request.user == review.user %}
                      <div class="d-flex justify-content-end col-12">
              <form action="{% url 'community:review_update' review.id %}" class="mx-5 my-5">
                  <input type="submit" value="수정">
              </form>
              <form action="{% url 'community:review_delete' review.id %}" method="POST" class="mx-5 my-5">
                  {% csrf_token %}
                  <input type="submit" value="삭제">
              </form>
              </div>
          {% endif %}
      {% if request.user.is_authenticated %}
      <div class="col-12 mb-5">
      <form action="{% url 'community:comments_create' review.id%}" method="POST">
          {% csrf_token %}
          {{ form.as_p }}
          <input type="submit" value="댓글 작성">
      </form>
      </div>
      {% endif %}
      <hr>
      {% for comment in review.comment_set.all %}
          <div class="border border-dark col-12 row my-2">
          <div class="col-2 py-2">댓글내용</div> <div class="col-3 py-2">: {{comment.content}}</div>
          <div class="col-3 py-2">작성자 : {{comment.user.username}}</div>
          <div class="col-4 py-2">
          {% if request.user == comment.user %}
          <form action="{% url 'community:comments_delete' review.id comment.id %}" method="POST">
              {% csrf_token %}
              <input type="submit" value="삭제">
          </form>
          {% endif %}
          </div>
          </div>
      
      {% endfor %}
      
      {% endblock %}
      ```

    - `review_list.html`

      ```html
      {% extends 'base.html' %}
      {% block body %}
      
      <div id="carouselExampleControls" class="carousel slide mt-2" data-ride="carousel">
        <div class="carousel-inner">
          <div class="carousel-item active">
            <img src="https://images.hdqwalls.com/wallpapers/bthumb/1917-movie-2020-9k.jpg" class="d-block w-100" alt="...">
          </div>
          <div class="carousel-item">
            <img src="https://mcdn.wallpapersafari.com/medium/22/0/Bnaz3x.jpg" class="d-block w-100" alt="...">
          </div>
          <div class="carousel-item">
            <img src="https://c.wallhere.com/photos/0b/1a/1536x864_px_BB_8_Captain_Phasma_chewbacca_Han_Solo_Kylo_Ren_Lightsaber_Movie_Poster-628419.jpg!d" class="d-block w-100" alt="...">
          </div>
      
          <div class="carousel-item">
            <img src="http://tiledwallpaper.com/wallpapers/2018/1/1391622955a5c2ce001c758.71036061_thumb.jpg" class="d-block w-100" alt="...">
          </div>
      
      
          <div class="carousel-item">
            <img src="http://tiledwallpaper.com/wallpapers/2017/6/63830082259366cf99b29e7.58116313_thumb.jpg" class="d-block w-100" alt="...">
          </div>
        </div>
      
      
        <a class="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="sr-only">Previous</span>
        </a>
        <a class="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="sr-only">Next</span>
        </a>
      </div>
      
      
      
      
      
      
      
      
      <div class="text-center h1 col-6 offset-3 mt-5 mb-5" style="border-bottom: 2px solid">영화 리뷰 게시판</div>
      
      <table class="table mx-auto table-bordered mt-5">
        <thead class="thead-light">
          <tr>
            <th scope="col" class="text-center">번호</th>
            <th scope="col" class="text-center">영화제목</th>
            <th scope="col" class="text-center">글 제목</th>
            <th scope="col" class="text-center">작성시간</th>
            <th scope="col" class="text-center">작성자</th>
          </tr>
        </thead>
        <tbody>
      
          {% for review in reviews %}
              <tr>
                <th scope="row" class="text-center">{{ forloop.revcounter }}</th>
                <td>{{ review.movie_title }}</td>
                <td><a href="{% url 'community:review_detail' review.id %}" class="text-dark text-decoration-none ">{{ review.title }}</a></td>
                <td>{{ review.created_at }}</td>
              <td>{{ review.user.username }}</td>
              </tr>
      
          {% endfor %}
            </tbody>
      </table>
      
      <div class="text-right my-5"><a href="{% url 'community:review_create' %}" class="h2 text-decoration-none text-dark">글 작성하러가기</a></div>
      
      {% endblock %}
      ```

    - `admin.py`

      ```python
      from django.contrib import admin
      from .models import Review,Comment
      # Register your models here.
      
      
      class ReviewAdmin(admin.ModelAdmin):
          list_display=('title','content','created_at','updated_at','user')
      
      class CommentAdmin(admin.ModelAdmin):
          list_display=('content','created_at','updated_at','user')
      
      admin.site.register(Review,ReviewAdmin)
      admin.site.register(Comment,CommentAdmin)
      
      ```

      

## 4. 느낀 점

> 첫 Team 프로젝트로서 굉장히 재밌었고, 유익했다. 팀으로서, 개인으로서 느낀 점을 정리해보자.

- 팀으로서 느낀 점
  - 가장 먼저, 우리 반의 코왕 창완이 형님과 프로젝트를 진행하게 됐는데, 시작 전부터 걱정이 많았다. 실력 차이가 많이 나다보니 도움이 안되고 피해를 끼칠까봐, 혹시 내가 너무 답답해서 창완이형이 속상해하실까봐.. 그런데 절대 그렇지 않았다. 창완이형이 맞춤형 프로젝트를 진행해 줄 것을 말씀해 주셨기에....
  - Slack, Trello 등의 협업 Tool을 이용하는 것 부터, 쉬는시간도 서로 합의해서 갖자는 사소한 의사소통, 코드 작성 및 리뷰 등 이제 개발자로서 그래도 무언가 한다는 느낌이 솔직히 들었다(별거 아니겠지만)
  - 코드를 작성하고, 창완이형이 봐주시고 설명해주시고 하는 식으로 거의 다 흘러갔던 것 같다. 든든한 창완이형을 보니 다음 프로젝트때는 내가 누군가에게 이런 존재가 되어주고 싶었다..
  - 역량이 부족해도 창완이형한테 내가 해보겠다고 말씀 드리면서 고생을 많이 했는데, 창완이형이 다 이해해주시고 설명도 너무너무 잘해주시고 잘 이끌어주셔서 유익하고 재미있게 프로젝트를 했던 것 같다.
  - 7~9시 각자 식사 후 9시부터 10시까지는 프로젝트 하면서의 내용들을 서로 나누는 시간을 1시간정도 가졌다. 화상채팅을 통해서 진행했는데, 모르는 점은 보완하고 코드도 같이 보면서 같이 공부해서 좋았다.(가 아니라 내가 과외 받은거다.)
  - 확실히 개인 프로젝트보다 팀 프로젝트가 훨~~씬 재밌다. 물론 이번 프로젝트에서는 내가 팀원을 보완해줄 내용이 없어서 못느낀것도 많을 것 같긴 한데.. 나중에 실력이 비슷한 친구와 하게되면 서로 모르는 부분을 보완해주고 서로 검색해나가는 재미도 있을 것 같다는 생각이 든다.
  - 진짜 진짜 팀프로젝트 좋다!! 다음주에도 하고싶다.. 교수님이 안내주시면 스스로라도 해야징

- 개인으로서 느낀 점
  - 일단 많이 익숙해졌다라는 생각이 들었다. 언젠가 팀프로젝트가 있을 것이라고 생각했고, 그 때 피해를 끼치기 싫어서 수업시간에 한 내용을 기능 구현만큼은 익숙하게 하려고 혼자 연습을 많이 했었는데, 엄청 크게 막히는 부분 없이 비교적 수월하게 할 수 있었다.
- 특히, 기존 코드를 거의 안보면서 진행했는데, 물론 창완이형이 옆에 있어서 그럴 수 있었겠지만.. 스스로 성장한다는 것을 느낄 수 있었다.
  - 그런데 기본 틀을 제외하고 세부적인 부분들이 많이 부족하다는 것을 느꼈다. 특히 이론 부분이 그랬는데, 이 부분은 꼭 보완해야 할 것 같다. '코드 한 줄 한 줄까지는 다 몰라도 기능만 구현하면 장땡이지'라고 생각했었는데, 이제는 어느정도 익숙해진 만큼 이론의 학습과 함께 코드 한 줄 한 줄 생각하면서 개발해야겠다.
  - 여튼, 이번 프로젝트를 통해 CRUD 기능, 1:N 기능 흐름에 많이 익숙해질 수 있었고, 세부적인 코드들도 이해할 수 있는 좋은 시간이었다!
  - 창완이형 고생 많으셨습니다 ! 저 생각보다 나쁘지 않았죠? >_<
  - 빨리 다음 프로젝트도 하고싶다!!!!!!!!!!!!!!!!!!!!!!!!!
  - 끝!
  
  
  
  




<x-layoutAdm page='المقالات'>

        <article class="content">

            <h1 class="big-title" id="title">مراجعة المقالات </h1>

            @if ($articles->count())

                @foreach ($articles as $article)

                        <div class="listes-contenu">

                            <div class="image-caption">
                                <a href="{{ route('articles.show', $article) }}">
                                    @php
                                        $images = explode(",", $article->Myimage);
                    					$images = array_reverse($images)
                                    @endphp
                                    <img src="{{ asset('images/articles/'.$images[0]) }}"
                                        alt="{{ $article->title }}">
                                </a>
                            </div>
                            <div class="listes-contenu-art">
                                <a href="{{ route('articles.show', $article) }}">
                                    <div class="listes-title-contenu">
                                        <h2>{{ $article->title }}</h2>
                                        <p style="color:black; text-align:justify">
                                            &emsp;{{ Str::limit($article->Mydescription, 100, '...') }}
                                            <span
                                                style="color: #9d6e25;
                                                            justify-content: center;
                                                            font-family: Tahoma;">
                                                إقرأ المزيد
                                            </span>
                                        </p>
                                    </div>
                                </a>
                                <div style="display: flex; gap: 15px; align-items: center;">
                                    <form action="{{ route('articles.destroy', $article) }}" method="POST" style="margin: 0;">
                                        @csrf
                                        @method('DELETE')
                                        <button class="btn btn-danger">
                                            <i class="fas fa-trash-alt"></i> 
                                            حدف المقال
                                        </button>
                                    </form>

                                    <a href="{{ route('articles.show', $article) }}" class="btn btn-secondary">
                                        <i class="fas fa-book-open" ></i>
                                        قراءة المقال
                                    </a>

                                    <a href="{{ route('articles.edit', $article) }}" class="btn btn-primary">
                                        <i class="fas fa-edit"></i> تعديل المقال
                                    </a>
                                </div>
                            </div>
                        </div>
                        <hr>
                @endforeach
                <div class="pagination-wrapper">
                    {{ $articles->links('vendor.pagination.bootstrap-5') }}
                </div>
            @else
                <p>لا توجد مقالات حاليا !</p>
            @endif
        </article>
</x-layoutAdm>

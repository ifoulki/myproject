<x-layoutAdm page='رسالة {{ $msg->Author }}'>

    <style>
        .card {
    border-radius: 8px;
}

.card h3 {
    font-weight: bold;
}

.img-fluid {
    max-width: 100%;
    height: auto;
}

    .card {
        border-radius: 8px;
    }

    .card-body {
        font-size: 16px;
        line-height: 1.8;
    }

    .btn i {
        margin-right: 5px;
    }

    img.img-fluid {
        max-width: 20%;
        border-radius: 50%;
        border: solid 2px #007bff;
    }
    
    .text-center h1.text-primary {
        font-size: 28px;
        font-weight: bold;
    }
</style>    

    <article class="content" dir="{{$msg->dir}}">

    <div class="container mt-5">
        <div class="card shadow-sm border-0">
            <div class="row no-gutters">

                <div class="col-md-4 text-center d-flex align-items-center justify-content-center bg-light">
                    @php
                        $images = explode(',', $msg->author_img);
                    @endphp
                    <figure>
                        <img style="max-width: 80%; border-radius: 50%; border: solid 2px #007bff;"
                             src="{{ asset($images[0] ?? 'default-image.png') }}"
                             alt="{{ $msg->title }}"
                             class="img-fluid">
                             <figcaption class="text-muted mb-3"> {{ $msg->Author }}</figcaption>
                    </figure>
                </div>
                <div class="col-md-8 p-3">
                    @if ($msg->title!="standard")
                        <label class="text-muted mb-3">
                            @if ($msg->dir=="ltr")
                                Object :
                            @else
                                الموضوع :               
                            @endif
                        </label>
                            <h2 class="label">{{ $msg->title }}</h2>
                        @endif

                        <label class="text-muted mb-3">
                           @if ($msg->dir!="ltr")
                               نص الرسالة :             
                           @endif
                       </label>

                    <p class="text-justify">{!! $msg->Mysubject !!}</p>
                    <p class="text-justify text-muted">{!! $msg->autre !!}</p>

                    @php
                        $authorId=$msg->author_id;
                    @endphp 

                    <div class="d-flex justify-content-center gap-3 mb-2">
                        <button onclick="redirectToForm({{ $authorId }})" class="btn btn-primary">
                            <i class="fas fa-reply"></i> رد
                        </button>

                        <form action="{{ route('msgs.destroy', $msg) }}" method="POST">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-danger">
                                <i class="fas fa-trash-alt"></i> حذف
                            </button>
                        </form>
                    </div>

                    <a href="#" onclick="history.back(); return false;" class="btn btn-secondary">
                        <i class="fas fa-arrow-left"></i> العودة للصفحة السابقة
                    </a>
                </div>
            </div>
        </div>
    </div>
</article>

        <script>
            function redirectToForm(authorId) {
                const url = `/%D8%A7%D8%AA%D8%B5%D9%84_%D8%A8%D9%86%D8%A7?user_id=${authorId}`;
                window.location.href = url;
            }
        </script>
    </x-layoutAdm>

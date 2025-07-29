@php
    $lang = auth()->user()?->Language ?? 'Ar';
    $dir = $lang === 'Ar' ? 'rtl' : 'ltr';
    $langAttr = $lang === 'Ar' ? 'Ar' : ($lang === 'Fr' ? 'Fr' : 'En');
@endphp

<!DOCTYPE html>
<html lang="{{ $langAttr }}" dir="{{ $dir }}">
<head>
    <meta charset="UTF-8">
    <title>🛍️ 
        @if($lang == 'Fr')
            Détails du produit
        @elseif($lang == 'En')
            Product Details
        @else
            تفاصيل المنتج
        @endif
    </title>

    <!-- Bootstrap (RTL أو عادي حسب اللغة) -->
    @if($lang == 'Ar')
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    @else
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    @endif

    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
    
    <style>
        body {
            background-color: #f8f9fa;
            font-family: '{{ $lang == 'Ar' ? 'Cairo' : 'Arial' }}', sans-serif;
        }

        .language-selector {
            min-width: 140px;
            margin-bottom: 1rem;
            text-align: end;
        }
        .language-selector select {
            padding-left: 30px !important; /* لترك مساحة للأيقونة */
            background-repeat: no-repeat;
            background-position: 8px center;
            background-size: 20px 15px;
        }

        .product-card {
            background: #fff;
            border-radius: 15px;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
            overflow: hidden;
        }
        .product-images img {
            width: 100%;
            max-height: 400px;
            object-fit: contain;
            border-radius: 10px;
        }
        .thumbs img {
            width: 80px;
            height: 80px;
            object-fit: contain;
            cursor: pointer;
            border: 2px solid transparent;
            border-radius: 8px;
        }
        .thumbs img:hover {
            border-color: #0d6efd;
        }
        .price {
            font-size: 1.5rem;
            color: #28a745;
            font-weight: bold;
        }
        .old-price {
            text-decoration: line-through;
            color: #6c757d;
            margin-inline-end: 10px;
        }
    </style>
</head>
<body>

    <div class="container my-5">
          <!-- زر تغيير اللغة أعلى يمين الصفحة -->
        <form id="languageForm" method="POST" action="{{ route('user.language.update') }}" class="language-selector">
            @csrf
            <select name="Language" class="form-select d-inline-block w-auto" onchange="this.form.submit();" aria-label="اختيار اللغة">
                <option value="Ar" {{ $lang == 'Ar' ? 'selected' : '' }}>العربية 🇲🇦</option>
                <option value="Fr" {{ $lang == 'Fr' ? 'selected' : '' }}>Français 🇫🇷</option>
                <option value="En" {{ $lang == 'En' ? 'selected' : '' }}>English 🇬🇧</option>
            </select>
        </form>
        <div class="product-card p-4">
            <div class="row">
                <!-- الصور -->
                <div class="col-md-6">
                    <div class="product-images mb-3">
                        @php
                            $images = explode(',', $product->image_filenames);
                            $mainImage = asset('images/products/' . $images[0]);
                        @endphp
                        <img id="mainImage" src="{{ $mainImage }}" alt="Product Image">
                    </div>
                    <div class="thumbs d-flex gap-2 flex-wrap">
                        @foreach($images as $img)
                            <img src="{{ asset('images/products/' . $img) }}" onclick="document.getElementById('mainImage').src=this.src;">
                        @endforeach
                    </div>
                </div>
    
                <!-- المعلومات -->
                <div class="col-md-6">
                    <h2 class="mb-3">
                        <i class="fas fa-box-open me-2"></i>
                        {{
                            $lang == 'Fr' ? $product->name_in_french :
                            ($lang == 'En' ? $product->name : $product->name_in_arabic)
                        }}
                    </h2>
    
                    <p>
                        <strong>
                            {{ $lang == 'Fr' ? 'Catégorie' : ($lang == 'En' ? 'Category' : 'الفئة') }}:
                        </strong>
                        {{ $product->category }}
                    </p>
    
                    @php
                        $currency = match($lang) {
                            'Ar' => 'درهم',
                            'Fr' => 'Dh',
                            'En' => 'MAD',
                            default => 'MAD',
                        };
                    @endphp

                    <div class="mb-3">
                        @if($product->price_before_discount)
                            <span class="old-price">
                                {{ number_format($product->price_before_discount, 2) }} {{ $currency }}
                            </span>
                        @endif
                        <span class="price">
                            {{ number_format($product->selling_price, 2) }} {{ $currency }}
                        </span>
                    </div>

                    <p><strong>{{ $lang == 'Fr' ? 'Description' : ($lang == 'En' ? 'Description' : 'الوصف') }}:</strong></p>
                    <p>
                        {!! 
                            $lang == 'Fr' ? $product->french_description :
                            ($lang == 'En' ? $product->description : $product->arabic_description)
                        !!}
                    </p>
    
                    <a href="{{ route('auth.products.edit', $product->id) }}" class="btn btn-warning mt-3">
                        <i class="fas fa-edit"></i>
                        {{ $lang == 'Fr' ? 'Modifier le produit' : ($lang == 'En' ? 'Edit Product' : 'تعديل المنتج') }}
                    </a>
                </div>
            </div>
        </div>
    </div>=

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

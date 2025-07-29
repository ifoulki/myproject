@php
    $userLang = auth()->user()->Language ?? 'Ar'; // القيمة الافتراضية العربية
@endphp

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>قائمة المنتجات</title>


    <!-- Bootstrap RTL -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600&display=swap" rel="stylesheet">

    <style>
    
        @media (max-width: 576px) {
            .product-name {
                font-size: 1rem;
            }
            .product-sub {
                font-size: 0.75rem;
            }
            .page-header {
                padding: 15px 20px;
                font-size: 1.2rem;
            }
            
             .product-card img {
                height: auto;
            }
        }
    
        .container {
            max-width: 1200px;
            margin-top: 40px;
        }

        body {
            background-color: #f5f7fa;
            font-family: 'Cairo', sans-serif;
        }

        .container {
            max-width: 1200px;
            margin-top: 40px;
        }

        .page-header {
            background: linear-gradient(90deg, #0d6efd, #0dcaf0);
            color: #fff;
            padding: 25px 30px;
            border-radius: 12px;
            margin-bottom: 25px;
        }

        .product-card {
            transition: 0.3s ease-in-out;
            border: none;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
        }

        .product-card img {
            width: 100%;
            height: 200px;
            object-fit: contain;
            background-color: #f8f9fa;
            border-bottom: 1px solid #ddd;
        }


        .product-info {
            padding: 15px;
        }

        .product-name {
            font-size: 1.1rem;
            font-weight: 600;
        }

        .product-sub {
            color: gray;
            font-size: 0.85rem;
        }

        .search-filter {
            margin-bottom: 30px;
            background-color: #fff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
        }

        .btn-action {
            margin: 3px;
        }

        .add-to-cart-icon {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 6px 9px;
            border-radius: 50%;
            color: #198754;
            cursor: pointer;
            font-size: 18px;
            transition: background-color 0.3s;
        }

        .add-to-cart-icon:hover {
            background-color: #d1e7dd;
        }

        .product-checkbox {
            display: none;
        }
    </style>
</head>
<body>


<div class="container">
    <div class="page-header d-flex justify-content-between align-items-center">
        <div class="d-flex flex-column flex-md-row align-items-start align-items-md-center gap-3">
            <h3 class="mb-0"><i class="fas fa-store"></i> المنتجات</h3>
            <span class="badge bg-light text-dark fs-6 shadow-sm px-3 py-2">
                <i class="fas fa-boxes text-primary me-2"></i> عدد المنتجات: {{ $totalProducts }}
            </span>
        </div>
        
                <div class="d-flex align-items-center gap-3 flex-wrap">

         <!-- زر اختيار اللغة -->
            <form id="languageForm" method="POST" action="{{ route('user.language.update') }}" class="language-selector">
                @csrf
                <select name="Language" class="form-select" onchange="this.form.submit();" aria-label="اختيار اللغة">
                    <option value="Ar" {{ $userLang == 'Ar' ? 'selected' : '' }}>العربية 🇲🇦</option>
                    <option value="Fr" {{ $userLang == 'Fr' ? 'selected' : '' }}>Français 🇫🇷</option>
                    <option value="En" {{ $userLang == 'En' ? 'selected' : '' }}>English 🇬🇧</option>
                </select>
            </form>
        <a href="{{ route('auth.products.create') }}" class="btn btn-success">
            <i class="fas fa-plus-circle"></i> منتج جديد
        </a>
    </div>    
    </div>    

    <div class="text-center my-4">
        <button id="create-invoice-btn" class="btn btn-success">
            <i class="fas fa-file-invoice"></i> إنشاء الفاتورة
        </button>
    </div>

    <div class="search-filter row g-3 align-items-center">
        <div class="col-md-6">
            <form method="GET" action="{{ route('auth.products.index') }}">
                <div class="input-group">
                    <input type="text" name="search" value="{{ request('search') }}" class="form-control" placeholder="ابحث عن منتج...">
                    <button class="btn btn-primary" type="submit"><i class="fas fa-search"></i></button>
                </div>
            </form>
        </div>
        <div class="col-md-6">
            <form method="GET" action="{{ route('auth.products.index') }}">
                <div class="input-group">
                    <select name="category" onchange="this.form.submit()" class="form-select">
                        <option value="">كل الفئات</option>
                        @foreach($categories as $cat)
                            <option value="{{ $cat->category }}" {{ request('category') == $cat->category ? 'selected' : '' }}>
                                {{ $cat->category }} ({{ $cat->count }})
                            </option>
                        @endforeach
                    </select>
                    <button type="submit" class="btn btn-secondary">فلترة</button>
                </div>
            </form>
        </div>
    </div>

    @if(request('search') || request('category'))
        @php
            $searchTerm = request('search');
            $categoryTerm = request('category');
        @endphp
        <div class="alert alert-info mt-3 d-flex align-items-center justify-content-center gap-2" role="alert">
            <i class="fas fa-search text-primary"></i>
            <div>
                @if($userLang == 'Fr')
                    <strong>{{ $totalResults }}</strong> résultats trouvés 
                    @if($searchTerm)
                        pour "<strong>{{ $searchTerm }}</strong>"
                    @endif
                    @if($searchTerm && $categoryTerm)
                        et
                    @endif
                    @if($categoryTerm)
                        dans la catégorie "<strong>{{ $categoryTerm }}</strong>"
                    @endif
                @elseif($userLang == 'En')
                    <strong>{{ $totalResults }}</strong> results found 
                    @if($searchTerm)
                        for "<strong>{{ $searchTerm }}</strong>"
                    @endif
                    @if($searchTerm && $categoryTerm)
                        and
                    @endif
                    @if($categoryTerm)
                        in category "<strong>{{ $categoryTerm }}</strong>"
                    @endif
                @else
                    تم العثور على <strong>{{ $totalResults }}</strong> نتيجة 
                    @if($searchTerm)
                        لـ "<strong>{{ $searchTerm }}</strong>"
                    @endif
                    @if($searchTerm && $categoryTerm)
                        و
                    @endif
                    @if($categoryTerm)
                        في الفئة "<strong>{{ $categoryTerm }}</strong>"
                    @endif
                @endif
            </div>
        </div>
    @endif


        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4">
            @foreach($products as $product)
                <div class="col">
                    <input type="checkbox" class="product-checkbox" value="{{ $product->id }}">
                    <div class="card product-card h-100">
                        @php
                            $images = explode(',', $product->image_filenames);
                            $randomImage = $images[array_rand($images)];
                        @endphp
                        <a href="{{ route('auth.products.show', $product->id) }}">
                            <img src="{{ asset('images/products/' . $randomImage) }}" alt="صورة المنتج" class="card-img-top">
                        </a>
                     @if ($userLang == 'Ar')
                        <div dir="rtl"class="product-info"><div class="product-name">
                    @else
                        <div dir="ltr"class="product-info"><div class="product-name">
                    @endif
                            @if ($userLang == 'Fr')
                                {{ $product->name_in_french }}
                            @elseif ($userLang == 'En')
                                {{ $product->name }}
                            @else
                                {{ $product->name_in_arabic }}
                            @endif
                        </div>
                        
                        <div class="product-sub text-muted">
                            @if ($userLang == 'Fr')
                                {{ \Illuminate\Support\Str::limit($product->french_description, 60) }}
                            @elseif ($userLang == 'En')
                                {{ \Illuminate\Support\Str::limit($product->description, 60) }}
                            @else
                                {{ \Illuminate\Support\Str::limit($product->arabic_description, 60) }}
                            @endif
                        </div>

                            <div class="text-muted my-2"><i class="fas fa-layer-group"></i> {{ $product->category }}</div>
                                 @if ($userLang == 'Ar')
                                   <div class="fw-bold mb-3"><i class="fas fa-coins"></i> {{ number_format($product->selling_price, 2) }} د.م</div>
                                @else
                                    <div dir="ltr" class="fw-bold mb-3"><i class="fas fa-coins"></i> {{ number_format($product->selling_price, 2) }} MAD </div>
                                @endif
                            <div class="d-flex justify-content-between align-items-center">
                                <a href="{{ route('auth.products.edit', $product->id) }}" class="btn btn-warning btn-sm btn-action" title="تعديل">
                                    <i class="fas fa-edit"></i>
                                </a>

                                <i class="fas fa-cart-plus add-to-cart-icon {{ $product->inCart ? 'text-success' : 'text-muted' }}" 
                                    onclick="toggleCart(this)" 
                                    data-product-id="{{ $product->id }}"
                                    title="{{ $product->inCart ? 'إزالة من السلة' : 'إضافة إلى السلة' }}"></i>

                                <form action="{{ route('auth.products.destroy', $product->id) }}" method="POST" onsubmit="return confirm('هل أنت متأكد من الحذف؟');">
                                    @csrf
                                    @method('DELETE')
                                    <button type="submit" class="btn btn-danger btn-sm btn-action" title="حذف">
                                        <i class="fas fa-trash-alt"></i>
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            @endforeach
        </div>

        <div class="mt-4">
            {{ $products->links('pagination::bootstrap-5') }}
        </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
    function toggleCart(iconElement) {
    const productId = iconElement.getAttribute('data-product-id');
    
    fetch('/cart/toggle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': '{{ csrf_token() }}'
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'added') {
            iconElement.classList.remove('text-muted');
            iconElement.classList.add('text-success');
            iconElement.title = 'إزالة من السلة';
        } else {
            iconElement.classList.remove('text-success');
            iconElement.classList.add('text-muted');
            iconElement.title = 'إضافة إلى السلة';
        }
        updateCartCount();
    });
}

function updateCartCount() {
    fetch('/cart/count')
    .then(response => response.json())
    .then(data => {
        // يمكنك تحديث عداد السلة في واجهة المستخدم هنا
        console.log('Cart count:', data.count);
    });
}

// تحديث حالة الأيقونات عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.add-to-cart-icon').forEach(icon => {
        const productId = icon.getAttribute('data-product-id');
        // يمكنك هنا التحقق من حالة السلة لكل منتج عند التحميل
    });
    updateCartCount();
});

document.getElementById("create-invoice-btn").addEventListener("click", function () {
    window.location.href = "{{ route('auth/invoice.create') }}";
});
</script>

</body>
</html>

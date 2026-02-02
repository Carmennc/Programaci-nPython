from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(_):
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>🌱 Catálogo de Plantas - Home</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #e8f5e9; }
            .container { max-width: 800px; margin: 0 auto; background: white; 
                        padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            nav a { margin-right: 15px; text-decoration: none; color: #2e7d32; font-weight: bold; }
            h1 { color: #1b5e20; }
            .product-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0; }
            .product { border: 1px solid #ddd; padding: 15px; border-radius: 5px; background: #f1f8e9; }
            .price { color: #388e3c; font-weight: bold; font-size: 1.1em; }
        </style>
    </head>
    <body>
        <div class="container">
            <nav>
                <a href="/static-pages/">🏠 Home</a>
                <a href="/static-pages/about/">ℹ️ About</a>
                <a href="/static-pages/contact/">📧 Contact</a>
                <a href="/dynamic-pages/">🎨 Catálogo Dinámico</a>
                <a href="/api/plantas/">🔌 API</a>
            </nav>
            
            <h1>🌱 Bienvenido a Plantas Catalog</h1>
            <p><strong>¿Qué es contenido estático?</strong></p>
            <ul>
                <li>✅ HTML completamente fijo</li>
                <li>✅ No consulta base de datos</li>
                <li>✅ Respuesta muy rápida</li>
                <li>✅ Ideal para landing pages</li>
            </ul>
            
            <h3>🌸 Plantas Destacadas (Estáticas)</h3>
            <div class="product-grid">
                <div class="product">
                    <h4>🌹 Rosa</h4>
                    <p>Riego: 3 veces/semana | Tamaño: 90 cm</p>
                    <p>Requerimiento: Luz solar directa</p>
                    <p class="price">$ 12.000</p>
                </div>
                <div class="product">
                    <h4>🌵 Aloe Vera</h4>
                    <p>Riego: 2 veces/semana | Tamaño: 60 cm</p>
                    <p>Requerimiento: Luz solar indirecta</p>
                    <p class="price">$ 12.000</p>
                </div>
            </div>
            
            <p><em>Esta página está definida directamente en el código Python.</em></p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)


def about(_):
    """Página About estática"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>📋 Acerca de</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #e8f5e9; }
            .container { max-width: 600px; margin: 0 auto; background: white; 
                        padding: 30px; border-radius: 10px; }
            h1 { color: #1b5e20; }
            a { color: #2e7d32; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📋 Acerca del Catálogo de Plantas</h1>
            <p>Esta es una página estática creada con Django.</p>
            <p><strong>Características:</strong></p>
            <ul>
                <li>No usa base de datos</li>
                <li>HTML fijo definido en views.py</li>
                <li>Respuesta inmediata</li>
                <li>Catálogo de plantas con especificaciones de cuidado</li>
            </ul>
            <a href="/static-pages/">← Volver al Home</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)
document.addEventListener('DOMContentLoaded', function() {
    // Lógica original para o checkbox de menor de idade
    var menorIdadeCheckbox = document.getElementById('menor_idade');
    if (menorIdadeCheckbox) {
        menorIdadeCheckbox.addEventListener('change', function() {
            var responsavelFields = document.getElementById('responsavel-fields');
            var responsavelInputs = responsavelFields.querySelectorAll('input');
            if (this.checked) {
                responsavelFields.style.display = 'block';
                responsavelInputs.forEach(function(input) {
                    input.required = true;
                });
            } else {
                responsavelFields.style.display = 'none';
                responsavelInputs.forEach(function(input) {
                    input.required = false;
                });
            }
        });
    }

    // Lógica essencial para o menu de ações da engrenagem
    var actionToggles = document.querySelectorAll('.actions-dropdown-toggle');

    actionToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(event) {
            event.stopPropagation();
            var menu = this.nextElementSibling;

            // Fecha outros menus abertos
            document.querySelectorAll('.actions-dropdown-menu.show').forEach(function(openMenu) {
                if (openMenu !== menu) {
                    openMenu.classList.remove('show');
                }
            });

            menu.classList.toggle('show');
        });
    });

    // Fecha o menu se o usuário clicar fora dele
    window.addEventListener('click', function(event) {
        var openMenus = document.querySelectorAll('.actions-dropdown-menu.show');
        openMenus.forEach(function(menu) {
            if (!menu.parentElement.contains(event.target)) {
                menu.classList.remove('show');
            }
        });
    });

    // Lógica para fechar flash messages automaticamente
    var flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        setTimeout(function() {
            flashMessages.forEach(function(message) {
                // Adiciona uma classe para animar o fade-out
                message.style.transition = 'opacity 0.5s ease';
                message.style.opacity = '0';
                // Remove o elemento após a animação
                setTimeout(function() {
                    message.remove();
                }, 500);
            });
        }, 5000); // 5 segundos
    }
});

hljs.registerLanguage("move", (hljs) => {
    const KEYWORDS = [
        "module",
        "struct",
        "as",
        "break",
        "const",
        "continue",
        "else",
        "enum",
        "false",
        "fun",
        "for",
        "if",
        "in",
        "let",
        "loop",
        "match",
        "module",
        "move",
        "mut",
        "public",
        "ref",
        "return",
        "self",
        "Self",
        "struct",
        "true",
        "type",
        "use",
        "while",
        "has",
        "entry",
        "acquires",
        "vector"
    ];
    const LITERALS = [
        "true",
        "false",
        "u8",
        "u16",
        "u32",
        "u64",
        "u128",
        "u256",
        "bool",
        "address",
        "signer",
        "Option",
        "String",
    ];
    const BUILTINS = [
        // abilities
        'copy',
        'drop',
        'key',
        'store',
        // macros
        "assert!",
    ];
    const TYPES = [];
    return {
        name: 'Move',
        aliases: ['mv'],
        keywords: {
            type: TYPES.join(' '),
            keyword: KEYWORDS.join(' '),
            literal: LITERALS.join(' '),
            built_in: BUILTINS.join(' ')
        },
        illegal: '</',
        contains: [
            hljs.NUMBER_MODE,
            hljs.C_LINE_COMMENT_MODE,
            hljs.COMMENT('/\\*', '\\*/', {contains: ['self']}),
            hljs.inherit(hljs.QUOTE_STRING_MODE, {
                begin: /[bx]?"/,
                illegal: null
            }),
            {
                className: 'symbol',
                begin: /\#\[/,
                end: /]/,
            },
            {
                className: 'meta',
                begin: '#!?\\[',
                end: '\\]',
                contains: [
                    {
                        className: 'string',
                        begin: /"/,
                        end: /"/,
                        contains: [
                            hljs.BACKSLASH_ESCAPE
                        ]
                    }
                ]
            },
            {
                begin: hljs.IDENT_RE + '::',
                keywords: {
                    keyword: "Self",
                    built_in: BUILTINS.join(' '),
                    type: TYPES.join(' ')
                }
            },
        ]
    };
});
hljs.initHighlightingOnLoad();
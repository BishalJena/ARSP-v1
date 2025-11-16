'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { DashboardLayout } from '@/components/dashboard-layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { useAuthenticatedAPI } from '@/lib/api-client-auth';
import { useLingo } from '@/lib/useLingo';
import {
  ArrowLeft, FileText, Calendar, Users, Building2,
  BookOpen, FlaskConical, BarChart3, MessageSquare,
  CheckCircle2, Lightbulb, AlertTriangle, Code, Trash2, Loader2
} from 'lucide-react';

// Section heading translations
const SECTION_TRANSLATIONS: Record<string, Record<string, string>> = {
  analyzed: {
    en: 'Analyzed',
    hi: 'विश्लेषित',
    te: 'విశ్లేషించబడింది',
    ta: 'பகுப்பாய்வு செய்யப்பட்டது',
    bn: 'বিশ্লেষিত',
    mr: 'विश्लेषण केले',
    zh: '已分析',
    es: 'Analizado',
    fr: 'Analysé',
    de: 'Analysiert',
    pt: 'Analisado',
    ja: '分析済み',
    ko: '분석됨',
    ru: 'Проанализировано',
    ar: 'تم التحليل'
  },
  tldr: {
    en: 'TL;DR',
    hi: 'संक्षेप में',
    te: 'సారాంశం',
    ta: 'சுருக்கம்',
    bn: 'সংক্ষেপে',
    mr: 'सारांश',
    zh: '简而言之',
    es: 'Resumen',
    fr: 'Résumé',
    de: 'Zusammenfassung',
    pt: 'Resumo',
    ja: '要約',
    ko: '요약',
    ru: 'Краткое содержание',
    ar: 'باختصار'
  },
  abstract: {
    en: 'Abstract',
    hi: 'सार',
    te: 'సారాంశం',
    ta: 'சுருக்கம்',
    bn: 'সারসংক্ষেপ',
    mr: 'गोषवारा',
    zh: '摘要',
    es: 'Resumen',
    fr: 'Résumé',
    de: 'Zusammenfassung',
    pt: 'Resumo',
    ja: '概要',
    ko: '초록',
    ru: 'Аннотация',
    ar: 'ملخص'
  },
  introduction: {
    en: 'Introduction & Background',
    hi: 'परिचय और पृष्ठभूमि',
    te: 'పరిచయం & నేపథ్యం',
    ta: 'அறிமுகம் & பின்னணி',
    bn: 'ভূমিকা ও পটভূমি',
    mr: 'परिचय आणि पार्श्वभूमी',
    zh: '介绍与背景',
    es: 'Introducción y Antecedentes',
    fr: 'Introduction et Contexte',
    de: 'Einführung & Hintergrund',
    pt: 'Introdução e Contexto',
    ja: '序論と背景',
    ko: '소개 및 배경',
    ru: 'Введение и предпосылки',
    ar: 'المقدمة والخلفية'
  },
  researchQuestion: {
    en: 'Research Question',
    hi: 'अनुसंधान प्रश्न',
    te: 'పరిశోధన ప్రశ్న',
    ta: 'ஆராய்ச்சி கேள்வி',
    bn: 'গবেষণা প্রশ্ন',
    mr: 'संशोधन प्रश्न',
    zh: '研究问题',
    es: 'Pregunta de Investigación',
    fr: 'Question de Recherche',
    de: 'Forschungsfrage',
    pt: 'Questão de Pesquisa',
    ja: '研究課題',
    ko: '연구 질문',
    ru: 'Исследовательский вопрос',
    ar: 'سؤال البحث'
  },
  methodology: {
    en: 'Methodology',
    hi: 'कार्यप्रणाली',
    te: 'పద్ధతి',
    ta: 'முறையியல்',
    bn: 'পদ্ধতি',
    mr: 'कार्यपद्धती',
    zh: '方法论',
    es: 'Metodología',
    fr: 'Méthodologie',
    de: 'Methodik',
    pt: 'Metodologia',
    ja: '方法論',
    ko: '방법론',
    ru: 'Методология',
    ar: 'المنهجية'
  },
  overview: {
    en: 'Overview',
    hi: 'अवलोकन',
    te: 'అవలోకనం',
    ta: 'மேலோட்டம்',
    bn: 'সংক্ষিপ্ত বিবরণ',
    mr: 'आढावा',
    zh: '概述',
    es: 'Descripción General',
    fr: 'Aperçu',
    de: 'Überblick',
    pt: 'Visão Geral',
    ja: '概要',
    ko: '개요',
    ru: 'Обзор',
    ar: 'نظرة عامة'
  },
  studyDesign: {
    en: 'Study Design',
    hi: 'अध्ययन डिजाइन',
    te: 'అధ్యయన రూపకల్పన',
    ta: 'ஆய்வு வடிவமைப்பு',
    bn: 'গবেষণা নকশা',
    mr: 'अभ्यास रचना',
    zh: '研究设计',
    es: 'Diseño del Estudio',
    fr: 'Conception de l\'Étude',
    de: 'Studiendesign',
    pt: 'Desenho do Estudo',
    ja: '研究デザイン',
    ko: '연구 설계',
    ru: 'Дизайн исследования',
    ar: 'تصميم الدراسة'
  },
  dataSources: {
    en: 'Data Sources',
    hi: 'डेटा स्रोत',
    te: 'డేటా మూలాలు',
    ta: 'தரவு ஆதாரங்கள்',
    bn: 'তথ্য উৎস',
    mr: 'डेटा स्रोत',
    zh: '数据来源',
    es: 'Fuentes de Datos',
    fr: 'Sources de Données',
    de: 'Datenquellen',
    pt: 'Fontes de Dados',
    ja: 'データソース',
    ko: '데이터 출처',
    ru: 'Источники данных',
    ar: 'مصادر البيانات'
  },
  sampleSize: {
    en: 'Sample Size',
    hi: 'नमूना आकार',
    te: 'నమూనా పరిమాణం',
    ta: 'மாதிரி அளவு',
    bn: 'নমুনা আকার',
    mr: 'नमुना आकार',
    zh: '样本量',
    es: 'Tamaño de Muestra',
    fr: 'Taille de l\'Échantillon',
    de: 'Stichprobengröße',
    pt: 'Tamanho da Amostra',
    ja: 'サンプルサイズ',
    ko: '표본 크기',
    ru: 'Размер выборки',
    ar: 'حجم العينة'
  },
  results: {
    en: 'Results',
    hi: 'परिणाम',
    te: 'ఫలితాలు',
    ta: 'முடிவுகள்',
    bn: 'ফলাফল',
    mr: 'निकाल',
    zh: '结果',
    es: 'Resultados',
    fr: 'Résultats',
    de: 'Ergebnisse',
    pt: 'Resultados',
    ja: '結果',
    ko: '결과',
    ru: 'Результаты',
    ar: 'النتائج'
  },
  keyFindings: {
    en: 'Key Findings',
    hi: 'मुख्य निष्कर्ष',
    te: 'ముఖ్య పరిశోధనలు',
    ta: 'முக்கிய கண்டுபிடிப்புகள்',
    bn: 'মূল ফলাফল',
    mr: 'मुख्य निष्कर्ष',
    zh: '主要发现',
    es: 'Hallazgos Clave',
    fr: 'Principales Conclusions',
    de: 'Hauptergebnisse',
    pt: 'Principais Descobertas',
    ja: '主な知見',
    ko: '주요 발견',
    ru: 'Основные выводы',
    ar: 'النتائج الرئيسية'
  },
  quantitativeResults: {
    en: 'Quantitative Results',
    hi: 'मात्रात्मक परिणाम',
    te: 'పరిమాణాత్మక ఫలితాలు',
    ta: 'அளவு முடிவுகள்',
    bn: 'পরিমাণগত ফলাফল',
    mr: 'परिमाणात्मक निकाल',
    zh: '定量结果',
    es: 'Resultados Cuantitativos',
    fr: 'Résultats Quantitatifs',
    de: 'Quantitative Ergebnisse',
    pt: 'Resultados Quantitativos',
    ja: '定量的結果',
    ko: '정량적 결과',
    ru: 'Количественные результаты',
    ar: 'النتائج الكمية'
  },
  discussion: {
    en: 'Discussion',
    hi: 'चर्चा',
    te: 'చర్చ',
    ta: 'விவாதம்',
    bn: 'আলোচনা',
    mr: 'चर्चा',
    zh: '讨论',
    es: 'Discusión',
    fr: 'Discussion',
    de: 'Diskussion',
    pt: 'Discussão',
    ja: '考察',
    ko: '논의',
    ru: 'Обсуждение',
    ar: 'مناقشة'
  },
  conclusion: {
    en: 'Conclusion',
    hi: 'निष्कर्ष',
    te: 'ముగింపు',
    ta: 'முடிவு',
    bn: 'উপসংহার',
    mr: 'निष्कर्ष',
    zh: '结论',
    es: 'Conclusión',
    fr: 'Conclusion',
    de: 'Schlussfolgerung',
    pt: 'Conclusão',
    ja: '結論',
    ko: '결론',
    ru: 'Заключение',
    ar: 'الخلاصة'
  },
  contributions: {
    en: 'Key Contributions',
    hi: 'मुख्य योगदान',
    te: 'ముఖ్య సహకారాలు',
    ta: 'முக்கிய பங்களிப்புகள்',
    bn: 'মূল অবদান',
    mr: 'मुख्य योगदान',
    zh: '主要贡献',
    es: 'Contribuciones Clave',
    fr: 'Contributions Clés',
    de: 'Hauptbeiträge',
    pt: 'Contribuições Principais',
    ja: '主な貢献',
    ko: '주요 기여',
    ru: 'Ключевые вклады',
    ar: 'المساهمات الرئيسية'
  },
  limitations: {
    en: 'Limitations',
    hi: 'सीमाएँ',
    te: 'పరిమితులు',
    ta: 'வரம்புகள்',
    bn: 'সীমাবদ্ধতা',
    mr: 'मर्यादा',
    zh: '局限性',
    es: 'Limitaciones',
    fr: 'Limitations',
    de: 'Einschränkungen',
    pt: 'Limitações',
    ja: '限界',
    ko: '한계',
    ru: 'Ограничения',
    ar: 'القيود'
  },
  practicalTakeaways: {
    en: 'Practical Takeaways',
    hi: 'व्यावहारिक निष्कर्ष',
    te: 'ఆచరణాత్మక సారాంశాలు',
    ta: 'நடைமுறை முடிவுகள்',
    bn: 'ব্যবহারিক শিক্ষা',
    mr: 'व्यावहारिक शिकवण',
    zh: '实用要点',
    es: 'Conclusiones Prácticas',
    fr: 'Points Pratiques',
    de: 'Praktische Erkenntnisse',
    pt: 'Conclusões Práticas',
    ja: '実用的な要点',
    ko: '실용적 시사점',
    ru: 'Практические выводы',
    ar: 'الاستنتاجات العملية'
  },
  futureWork: {
    en: 'Future Work',
    hi: 'भविष्य का कार्य',
    te: 'భవిష్యత్తు పని',
    ta: 'எதிர்கால பணி',
    bn: 'ভবিষ্যৎ কাজ',
    mr: 'भविष्यातील काम',
    zh: '未来工作',
    es: 'Trabajo Futuro',
    fr: 'Travaux Futurs',
    de: 'Zukünftige Arbeit',
    pt: 'Trabalho Futuro',
    ja: '今後の課題',
    ko: '향후 연구',
    ru: 'Будущая работа',
    ar: 'العمل المستقبلي'
  },
  glossary: {
    en: 'Glossary',
    hi: 'शब्दावली',
    te: 'పదకోశం',
    ta: 'சொற்களஞ்சியம்',
    bn: 'শব্দকোষ',
    mr: 'शब्दकोश',
    zh: '术语表',
    es: 'Glosario',
    fr: 'Glossaire',
    de: 'Glossar',
    pt: 'Glossário',
    ja: '用語集',
    ko: '용어집',
    ru: 'Глоссарий',
    ar: 'المسرد'
  },
  backToPapers: {
    en: 'Back to Papers',
    hi: 'पेपर्स पर वापस जाएं',
    te: 'పేపర్‌లకు తిరిగి వెళ్ళు',
    ta: 'ஆவணங்களுக்கு திரும்பு',
    bn: 'পেপারে ফিরে যান',
    mr: 'पेपर्सवर परत या',
    zh: '返回论文',
    es: 'Volver a Artículos',
    fr: 'Retour aux Articles',
    de: 'Zurück zu Papieren',
    pt: 'Voltar aos Artigos',
    ja: '論文に戻る',
    ko: '논문으로 돌아가기',
    ru: 'Вернуться к статьям',
    ar: 'العودة إلى الأوراق'
  },
  deletePaper: {
    en: 'Delete Paper',
    hi: 'पेपर हटाएं',
    te: 'పేపర్ తొలగించు',
    ta: 'ஆவணத்தை நீக்கு',
    bn: 'পেপার মুছুন',
    mr: 'पेपर हटवा',
    zh: '删除论文',
    es: 'Eliminar Artículo',
    fr: 'Supprimer l\'Article',
    de: 'Papier löschen',
    pt: 'Excluir Artigo',
    ja: '論文を削除',
    ko: '논문 삭제',
    ru: 'Удалить статью',
    ar: 'حذف الورقة'
  },
  translating: {
    en: 'Translating paper...',
    hi: 'पेपर का अनुवाद हो रहा है...',
    te: 'పేపర్ అనువదిస్తోంది...',
    ta: 'ஆவணம் மொழிபெயர்க்கப்படுகிறது...',
    bn: 'পেপার অনুবাদ হচ্ছে...',
    mr: 'पेपर भाषांतर होत आहे...',
    zh: '正在翻译论文...',
    es: 'Traduciendo artículo...',
    fr: 'Traduction en cours...',
    de: 'Papier wird übersetzt...',
    pt: 'Traduzindo artigo...',
    ja: '論文を翻訳中...',
    ko: '논문 번역 중...',
    ru: 'Перевод статьи...',
    ar: 'جاري ترجمة الورقة...'
  },
  translatingNote: {
    en: 'This will take 1-2 seconds. Future switches to this language will be instant!',
    hi: 'इसमें 1-2 सेकंड लगेंगे। भविष्य में इस भाषा में बदलाव तुरंत होगा!',
    te: 'దీనికి 1-2 సెకన్లు పడుతుంది. భవిష్యత్తులో ఈ భాషకు మారడం తక్షణమే జరుగుతుంది!',
    ta: 'இது 1-2 வினாடிகள் எடுக்கும். இந்த மொழிக்கு எதிர்கால மாற்றங்கள் உடனடியாக இருக்கும்!',
    bn: 'এতে 1-2 সেকেন্ড লাগবে। ভবিষ্যতে এই ভাষায় পরিবর্তন তাৎক্ষণিক হবে!',
    mr: 'यास 1-2 सेकंद लागतील. भविष्यात या भाषेत बदल त्वरित होईल!',
    zh: '这将需要1-2秒。将来切换到此语言将是即时的！',
    es: 'Esto tomará 1-2 segundos. ¡Los futuros cambios a este idioma serán instantáneos!',
    fr: 'Cela prendra 1-2 secondes. Les futurs changements vers cette langue seront instantanés!',
    de: 'Dies dauert 1-2 Sekunden. Zukünftige Wechsel zu dieser Sprache erfolgen sofort!',
    pt: 'Isso levará 1-2 segundos. Futuras mudanças para este idioma serão instantâneas!',
    ja: 'これには1〜2秒かかります。今後この言語への切り替えは即座に行われます！',
    ko: '1-2초가 걸립니다. 앞으로 이 언어로의 전환은 즉시 이루어집니다!',
    ru: 'Это займет 1-2 секунды. Будущие переключения на этот язык будут мгновенными!',
    ar: 'سيستغرق هذا 1-2 ثانية. ستكون التبديلات المستقبلية إلى هذه اللغة فورية!'
  }
};

// Helper function to get translated heading
const getHeading = (key: string, locale: string): string => {
  return SECTION_TRANSLATIONS[key]?.[locale] || SECTION_TRANSLATIONS[key]?.['en'] || key;
};

interface PaperAnalysis {
  // Metadata
  paper_id: string;
  paper_title: string;
  year?: number;
  authors?: string[];
  venue?: string;

  // Content from analysis JSONB
  analysis: {
    title: string;
    abstract?: string;
    introduction?: string;
    tldr?: string;
    research_question?: string;
    methods?: {
      overview?: string;
      data_sources?: string;
      sample_size?: string;
      study_design?: string;
    };
    results?: {
      summary?: string;
      key_findings?: string[];
      quantitative_results?: string[];
    };
    discussion?: string;
    conclusion?: string;
    limitations?: string[];
    contributions?: string[];
    practical_takeaways?: string[];
    future_work?: string[];
    glossary?: Record<string, string>;
  };
}

export default function PaperDetailPage() {
  const params = useParams();
  const router = useRouter();
  const apiClient = useAuthenticatedAPI();
  const { locale, t } = useLingo();

  const [paper, setPaper] = useState<PaperAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [translating, setTranslating] = useState(false);
  const [error, setError] = useState('');
  const [deleting, setDeleting] = useState(false);
  const [previousLocale, setPreviousLocale] = useState(locale);

  const paperId = params.id as string;

  useEffect(() => {
    fetchPaperAnalysis();
  }, [paperId, locale]);

  const fetchPaperAnalysis = async () => {
    // If we already have paper loaded, this is a translation request
    const isTranslation = paper !== null && locale !== previousLocale;

    if (isTranslation) {
      setTranslating(true);
    } else {
      setLoading(true);
    }

    try {
      const response = await apiClient.getPaper(paperId, { language: locale });
      setPaper(response);
      setPreviousLocale(locale);
    } catch (err: any) {
      setError(err.message || 'Failed to load paper analysis');
    } finally {
      setLoading(false);
      setTranslating(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this paper? This action cannot be undone.')) {
      return;
    }

    setDeleting(true);
    try {
      await apiClient.deletePaper(paperId);
      router.push('/dashboard/papers');
    } catch (err: any) {
      setError(err.message || 'Failed to delete paper');
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="space-y-6">
          <Skeleton className="h-12 w-full" />
          <Skeleton className="h-64 w-full" />
          <Skeleton className="h-64 w-full" />
        </div>
      </DashboardLayout>
    );
  }

  if (error || !paper) {
    return (
      <DashboardLayout>
        <div className="max-w-2xl mx-auto">
          <div className="text-center py-12">
            <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {error || 'Paper not found'}
            </h3>
            <p className="text-gray-600 mb-6">
              This paper may have failed to process or is no longer available.
            </p>
            <div className="flex items-center justify-center gap-4">
              <Button
                variant="outline"
                onClick={() => router.push('/dashboard/papers')}
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                {getHeading('backToPapers', locale)}
              </Button>
              <Button
                variant="destructive"
                onClick={handleDelete}
                disabled={deleting}
              >
                {deleting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Deleting...
                  </>
                ) : (
                  <>
                    <Trash2 className="mr-2 h-4 w-4" />
                    Delete This Paper
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  const analysis = paper.analysis || {};

  return (
    <DashboardLayout>
      <div className="max-w-5xl mx-auto space-y-6">
        {/* Translation Loading Banner */}
        {translating && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center gap-3">
              <Loader2 className="h-5 w-5 text-blue-600 animate-spin" />
              <div>
                <p className="text-sm font-medium text-blue-900">
                  {getHeading('translating', locale)}
                </p>
                <p className="text-xs text-blue-700">
                  {getHeading('translatingNote', locale)}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Header */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <Button
              variant="ghost"
              onClick={() => router.push('/dashboard/papers')}
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              {getHeading('backToPapers', locale)}
            </Button>

            <Button
              variant="destructive"
              onClick={handleDelete}
              disabled={deleting}
            >
              {deleting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Deleting...
                </>
              ) : (
                <>
                  <Trash2 className="mr-2 h-4 w-4" />
                  {getHeading('deletePaper', locale)}
                </>
              )}
            </Button>
          </div>

          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-8 border-2 border-blue-200">
            <div className="flex items-start justify-between mb-4">
              <FileText className="h-8 w-8 text-blue-600" />
              <Badge variant="default" className="bg-green-600">
                {getHeading('analyzed', locale)}
              </Badge>
            </div>

            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              {paper.paper_title || analysis.title}
            </h1>

            <div className="flex flex-wrap gap-4 text-sm text-gray-600">
              {paper.year && (
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  <span>{paper.year}</span>
                </div>
              )}
              {paper.authors && paper.authors.length > 0 && (
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4" />
                  <span>{paper.authors.slice(0, 3).join(', ')}{paper.authors.length > 3 ? ` +${paper.authors.length - 3} more` : ''}</span>
                </div>
              )}
              {paper.venue && (
                <div className="flex items-center gap-2">
                  <Building2 className="h-4 w-4" />
                  <span>{paper.venue}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* TL;DR */}
        {analysis.tldr && (
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-purple-900">
                <Lightbulb className="h-5 w-5" />
                {getHeading('tldr', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-800 leading-relaxed">{analysis.tldr}</p>
            </CardContent>
          </Card>
        )}

        {/* Abstract */}
        {analysis.abstract && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-blue-600" />
                {getHeading('abstract', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                {analysis.abstract}
              </p>
            </CardContent>
          </Card>
        )}

        {/* Introduction */}
        {analysis.introduction && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-green-600" />
                {getHeading('introduction', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                {analysis.introduction}
              </p>
            </CardContent>
          </Card>
        )}

        {/* Research Question */}
        {analysis.research_question && (
          <Card className="border-2 border-amber-200 bg-amber-50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-amber-900">
                <AlertTriangle className="h-5 w-5" />
                {getHeading('researchQuestion', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-800 leading-relaxed font-medium">
                {analysis.research_question}
              </p>
            </CardContent>
          </Card>
        )}

        {/* Methods */}
        {analysis.methods && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FlaskConical className="h-5 w-5 text-purple-600" />
                {getHeading('methodology', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {analysis.methods.overview && (
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">{getHeading('overview', locale)}</h4>
                  <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                    {analysis.methods.overview}
                  </p>
                </div>
              )}
              {analysis.methods.study_design && (
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">{getHeading('studyDesign', locale)}</h4>
                  <p className="text-gray-700">{analysis.methods.study_design}</p>
                </div>
              )}
              {analysis.methods.data_sources && (
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">{getHeading('dataSources', locale)}</h4>
                  <p className="text-gray-700">{analysis.methods.data_sources}</p>
                </div>
              )}
              {analysis.methods.sample_size && (
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">{getHeading('sampleSize', locale)}</h4>
                  <p className="text-gray-700">{analysis.methods.sample_size}</p>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Results */}
        {analysis.results && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-green-600" />
                {getHeading('results', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {analysis.results.summary && (
                <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                  {analysis.results.summary}
                </p>
              )}
              {analysis.results.key_findings && analysis.results.key_findings.length > 0 && (
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3">{getHeading('keyFindings', locale)}</h4>
                  <ul className="space-y-2">
                    {analysis.results.key_findings.map((finding, idx) => (
                      <li key={idx} className="flex gap-3">
                        <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                        <span className="text-gray-700">{finding}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {analysis.results.quantitative_results && analysis.results.quantitative_results.length > 0 && (
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3">{getHeading('quantitativeResults', locale)}</h4>
                  <ul className="space-y-2">
                    {analysis.results.quantitative_results.map((result, idx) => (
                      <li key={idx} className="flex gap-3">
                        <span className="text-blue-600 font-mono">→</span>
                        <span className="text-gray-700">{result}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Discussion */}
        {analysis.discussion && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MessageSquare className="h-5 w-5 text-indigo-600" />
                {getHeading('discussion', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                {analysis.discussion}
              </p>
            </CardContent>
          </Card>
        )}

        {/* Conclusion */}
        {analysis.conclusion && (
          <Card className="border-2 border-green-200 bg-green-50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-green-900">
                <CheckCircle2 className="h-5 w-5" />
                {getHeading('conclusion', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-800 leading-relaxed whitespace-pre-line">
                {analysis.conclusion}
              </p>
            </CardContent>
          </Card>
        )}

        {/* Contributions */}
        {analysis.contributions && analysis.contributions.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Lightbulb className="h-5 w-5 text-yellow-600" />
                {getHeading('contributions', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {analysis.contributions.map((contribution, idx) => (
                  <li key={idx} className="flex gap-3">
                    <span className="text-yellow-600 font-bold">•</span>
                    <span className="text-gray-700">{contribution}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}

        {/* Limitations */}
        {analysis.limitations && analysis.limitations.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-orange-600" />
                {getHeading('limitations', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {analysis.limitations.map((limitation, idx) => (
                  <li key={idx} className="flex gap-3">
                    <span className="text-orange-600 font-bold">⚠</span>
                    <span className="text-gray-700">{limitation}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}

        {/* Practical Takeaways */}
        {analysis.practical_takeaways && analysis.practical_takeaways.length > 0 && (
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-blue-900">
                <Lightbulb className="h-5 w-5" />
                {getHeading('practicalTakeaways', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {analysis.practical_takeaways.map((takeaway, idx) => (
                  <li key={idx} className="flex gap-3">
                    <span className="text-blue-600 font-bold">💡</span>
                    <span className="text-gray-800">{takeaway}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}

        {/* Future Work */}
        {analysis.future_work && analysis.future_work.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code className="h-5 w-5 text-purple-600" />
                {getHeading('futureWork', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {analysis.future_work.map((work, idx) => (
                  <li key={idx} className="flex gap-3">
                    <span className="text-purple-600 font-bold">→</span>
                    <span className="text-gray-700">{work}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}

        {/* Glossary */}
        {analysis.glossary && Object.keys(analysis.glossary).length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-gray-600" />
                {getHeading('glossary', locale)}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="space-y-3">
                {Object.entries(analysis.glossary).map(([term, definition]) => (
                  <div key={term} className="border-l-4 border-gray-300 pl-4">
                    <dt className="font-semibold text-gray-900">{term}</dt>
                    <dd className="text-gray-700 mt-1">{definition}</dd>
                  </div>
                ))}
              </dl>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}

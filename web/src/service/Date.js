import { useAuthStore } from '@/stores/AuthStore';
import { useSystemStore } from '@/stores/SystemStore';
import { format } from 'date-fns';
import { formatInTimeZone } from 'date-fns-tz';
import { de, enUS, es, fr, it, ja, ptBR, zhCN } from 'date-fns/locale';

const locales = {
    'en-US': enUS,
    'pt-BR': ptBR,
    'es-ES': es,
    'fr-FR': fr,
    'de-DE': de,
    'it-IT': it,
    'ja-JP': ja,
    'zh-CN': zhCN
};

export const ServiceDate = {
    parseSafeDate(date) {
        if (!date) return null;
        if (typeof date === 'string') {
            const cleaned = date.replace(/(\.\d{3})\d+Z$/, '$1Z');
            const parsed = new Date(cleaned);
            return isNaN(parsed) ? null : parsed;
        }
        if (date instanceof Date) {
            return isNaN(date.getTime()) ? null : date;
        }
        return null;
    },

    utc() {
        try {
            return new Date().toISOString();
        } catch (error) {
            throw new Error(`Erro ao obter data UTC: ${error.message}`);
        }
    },

    formatted(date, formatString = 'yyyy-MM-dd', timeZone = null) {
        try {
            const { metadata: authSettings } = useAuthStore();
            const { settings: systemSettings } = useSystemStore();
            const parsedDate = this.parseSafeDate(date);
            if (!parsedDate) return null;

            const tz = timeZone || authSettings.timezone || systemSettings.timezone || 'UTC';
            const localeCode = authSettings.locale || systemSettings.locale || 'pt-BR';
            const locale = locales[localeCode] || ptBR;

            return formatInTimeZone(parsedDate, tz, formatString, { locale });
        } catch (error) {
            throw new Error(`Erro ao formatar data no fuso horário: ${error.message}`);
        }
    },

    formatDateTime(date, formatString = 'yyyy-MM-dd HH:mm:ss') {
        try {
            const { metadata: authSettings } = useAuthStore();
            const { settings: systemSettings } = useSystemStore();
            const parsedDate = this.parseSafeDate(date);
            if (!parsedDate) throw new Error('Data inválida ou não fornecida.');

            const localeCode = authSettings.locale || systemSettings.locale || 'pt-BR';
            const locale = locales[localeCode] || ptBR;

            return format(parsedDate, formatString, { locale });
        } catch (error) {
            throw new Error(`Erro ao formatar data e hora: ${error.message}`);
        }
    },

    formatTime(date, formatString = 'HH:mm:ss') {
        try {
            const { metadata: authSettings } = useAuthStore();
            const { settings: systemSettings } = useSystemStore();
            const parsedDate = this.parseSafeDate(date);
            if (!parsedDate) throw new Error('Data inválida ou não fornecida.');

            const localeCode = authSettings.locale || systemSettings.locale || 'pt-BR';
            const locale = locales[localeCode] || ptBR;

            return format(parsedDate, formatString, { locale });
        } catch (error) {
            throw new Error(`Erro ao formatar hora: ${error.message}`);
        }
    },

    formatOrNow(date, formatString = 'yyyy-MM-dd', timeZone = null) {
        try {
            const { metadata: authSettings } = useAuthStore();
            const { settings: systemSettings } = useSystemStore();
            const parsedDate = this.parseSafeDate(date) || new Date();

            const tz = timeZone || authSettings.timezone || systemSettings.timezone || 'UTC';
            const localeCode = authSettings.locale || systemSettings.locale || 'pt-BR';
            const locale = locales[localeCode] || ptBR;

            return formatInTimeZone(parsedDate, tz, formatString, { locale });
        } catch (error) {
            throw new Error(`Erro ao formatar ou usar data atual: ${error.message}`);
        }
    },

    formatIfTodayTimeOnly(date, fullFormat = 'dd/MM/yyyy HH:mm:ss', timeFormat = 'HH:mm:ss') {
        try {
            const { metadata: authSettings } = useAuthStore();
            const { settings: systemSettings } = useSystemStore();
            const parsedDate = this.parseSafeDate(date);
            if (!parsedDate) return '';

            const now = new Date();
            const isSameDay = parsedDate.getDate() === now.getDate() && parsedDate.getMonth() === now.getMonth() && parsedDate.getFullYear() === now.getFullYear();

            const localeCode = authSettings.locale || systemSettings.locale || 'pt-BR';
            const locale = locales[localeCode] || ptBR;

            return format(parsedDate, isSameDay ? timeFormat : fullFormat, { locale });
        } catch (error) {
            throw new Error(`Erro ao formatar data condicional: ${error.message}`);
        }
    }
};

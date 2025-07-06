// toast.js
import { useConfirm } from 'primevue/useconfirm';
import { useToast } from 'primevue/usetoast';

let toast;
let confirm;

export const initializeMessaging = () => {
    toast = useToast();
    confirm = useConfirm();
};

export const MessageBox = (message, title, severity = 'secondary', life = 10000) => {
    if (toast) {
        toast.add({
            severity,
            summary: title,
            detail: message,
            group: 'headless',
            life: life,
            styleClass: 'backdrop-blur-lg rounded-2xl'
        });
    } else {
        console.warn('Toast não inicializado');
    }
};

export const MessageSuccess = (message, title = 'Êxito', life = 10000) => {
    MessageBox(message, title, 'success', life);
};
export const MessageWarn = (message, title = 'Atenção', life = 10000) => {
    MessageBox(message, title, 'warn', life);
};
export const MessageError = (message, title = 'Erro', life = 10000) => {
    MessageBox(message, title, 'error', life);
    return;
};
export const MessageInfo = (message, title = 'Informação', life = 10000) => {
    MessageBox(message, title, 'info', life);
};

export const ConfirmBox = ({ message, header = 'Confirmar', icon = 'pi pi-exclamation-triangle', accept, reject, acceptLabel = 'Sim', rejectLabel = 'Cancelar' }) => {
    if (confirm) {
        confirm.require({
            message,
            header,
            icon,
            accept,
            reject,
            group: 'headless',
            acceptLabel,
            rejectLabel
        });
    } else {
        console.warn('Confirm não inicializado');
    }
};

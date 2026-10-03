/**
 * 解析后端返回的时间字符串。
 * 后端可能返回 "2026-10-03 18:00" 或 "2026-10-03T18:00" 两种形式。
 * @param {string|null|undefined} value - 原始时间值
 * @returns {Date|null} 解析后的 Date；入参为空或非法时返回 null
 */
export function parseTime(value) {
    if (!value) return null
    const raw = String(value)
    const normalized = raw.includes('T') ? raw : raw.replace(' ', 'T')
    const date = new Date(normalized)
    return Number.isNaN(date.getTime()) ? null : date
}

function pad(num) {
    return String(num).padStart(2, '0')
}

/**
 * 格式化为 "M月D日 HH:mm" 的短日期。
 * @param {string|null|undefined} value - 原始时间值
 * @returns {string} 格式化结果；无法解析时原样返回（空值返回空串）
 */
export function formatDateTime(value) {
    const date = parseTime(value)
    if (!date) return value ? String(value) : ''
    return `${date.getMonth() + 1}月${date.getDate()}日 ${pad(date.getHours())}:${pad(date.getMinutes())}`
}

/**
 * 将时间值转换为 <input type="datetime-local"> 需要的 "YYYY-MM-DDTHH:mm"。
 * @param {string|null|undefined} value - 原始时间值
 * @returns {string} 可直接绑定到 datetime-local 控件的值；无法解析时返回空串
 */
export function toInputDateTime(value) {
    const date = parseTime(value)
    if (!date) return ''
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
}

/**
 * 生成相对时间文案，例如“刚刚”“3 分钟前”“2 小时前”“5 天前”。
 * @param {string|null|undefined} value - 原始时间值
 * @returns {string} 相对时间文案；无法解析时返回空串
 */
export function relativeTime(value) {
    const date = parseTime(value)
    if (!date) return ''
    const diff = Date.now() - date.getTime()
    if (diff < 60 * 1000) return '刚刚'
    const minutes = Math.floor(diff / 60000)
    if (minutes < 60) return `${minutes} 分钟前`
    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `${hours} 小时前`
    const days = Math.floor(hours / 24)
    if (days < 30) return `${days} 天前`
    const months = Math.floor(days / 30)
    if (months < 12) return `${months} 个月前`
    return `${Math.floor(months / 12)} 年前`
}

/**
 * 计算截止时间的展示信息与紧急等级。
 * @param {string|null|undefined} value - 原始截止时间
 * @returns {{ text: string, hint: string, level: 'normal'|'soon'|'urgent'|'overdue' }|null}
 *   text：格式化后的截止时间；hint：“还剩 x 天 / 仅剩 x 小时 / 已过期”；
 *   level：overdue 已过期，urgent 24 小时内，soon 3 天内，normal 其他
 */
export function deadlineInfo(value) {
    const date = parseTime(value)
    if (!date) return null
    const diff = date.getTime() - Date.now()
    const minutes = Math.floor(diff / 60000)

    let level = 'normal'
    let hint = ''
    if (diff < 0) {
        level = 'overdue'
        hint = '已过期'
    } else if (minutes < 60) {
        level = 'urgent'
        hint = `仅剩 ${Math.max(minutes, 1)} 分钟`
    } else if (minutes < 24 * 60) {
        level = 'urgent'
        hint = `仅剩 ${Math.floor(minutes / 60)} 小时`
    } else {
        const days = Math.floor(minutes / (24 * 60))
        if (minutes < 3 * 24 * 60) level = 'soon'
        hint = `还剩 ${days} 天`
    }

    return { text: formatDateTime(value), hint, level }
}

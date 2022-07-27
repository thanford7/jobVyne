export const SECTION_TYPES = {
  TEXT: {
    key: 'TEXT',
    label: 'Text section',
    defaultData: { html_content: '' },
    usedFor: ['About us', 'Why work for us', 'Diversity & Inclusion']
  },
  ICON: {
    key: 'ICON',
    label: 'Icons section',
    defaultData: { header: null, html_content: '', icon: null },
    usedFor: ['Benefits', 'Values', 'Hiring process'],
    exampleImagePath: '/images/iconsSectionExample.png'
  },
  CAROUSEL: {
    key: 'CAROUSEL',
    label: 'Picture carousel section',
    defaultData: { header: null, picture_ids: [], is_allow_autoplay: false },
    usedFor: ['Company culture', 'Faces of employees'],
    exampleImagePath: '/images/carouselSectionExample.png'
  },
  ACCORDION: {
    key: 'ACCORDION',
    label: 'Accordion list section',
    defaultData: { header: null, html_content: '' },
    usedFor: ['FAQ'],
    exampleImagePath: '/images/accordionSectionExample.png'
  }
}

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="choice">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="ref">
<xsl:text>(</xsl:text>
<xsl:value-of select="."/>
<xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="hi[@rend='squarebrackets']">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="hi[@rend='q1']">
<xsl:text>"</xsl:text>
<xsl:value-of select="."/>
<xsl:text>"</xsl:text>
</xsl:template>

<xsl:template match="lg/l/q">
<xsl:text>"</xsl:text>
<xsl:value-of select="."/>
<xsl:text>"</xsl:text>
</xsl:template>

</xsl:stylesheet>
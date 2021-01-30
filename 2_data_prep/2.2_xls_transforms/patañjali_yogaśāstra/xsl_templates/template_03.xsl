<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="head">

{<xsl:value-of select="."/>}

</xsl:template>

<xsl:template match="trailer">

〈<xsl:value-of select="."/>〉

</xsl:template>

<xsl:template match="quote/p">

[<xsl:value-of select="parent::quote/@xml:id"/>.0]

"<xsl:value-of select="."/>"
</xsl:template>

<xsl:template match="div/p">

[<xsl:value-of select="parent::div/quote/@xml:id"/>.<xsl:number count="p"/>]

<xsl:value-of select="."/>
</xsl:template>

</xsl:stylesheet>
